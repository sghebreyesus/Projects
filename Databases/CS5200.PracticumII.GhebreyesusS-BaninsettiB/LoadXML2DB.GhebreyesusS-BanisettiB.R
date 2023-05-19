library(RSQLite)
library(XML)

## connect to SQLite database
dbFile = "Pubmed.db"
conn <- dbConnect(RSQLite::SQLite(), dbFile)

dbExecute(conn, "PRAGMA foreign_keys = ON")

## create journals, articles, authors and authorship table
dbExecute(conn, "CREATE TABLE Journals (
  JournalID INTEGER PRIMARY KEY AUTOINCREMENT,
  ISSN TEXT,
  Title TEXT,
  IssnType TEXT,
  CitedMedium TEXT,
  PubDate Date,
  ISOAbbreviation TEXT)"
)

dbExecute(conn, "CREATE TABLE Articles (
  ArticleID INTEGER PRIMARY KEY AUTOINCREMENT,
  ArticleTitle TEXT,
  JournalID INTEGER,
  FOREIGN KEY (JournalID) references Journals(JournalID))"
)

dbExecute(conn, "CREATE TABLE Authors (
  AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
  LastName TEXT, 
  ForeName TEXT,
  Initials TEXT)"
)

dbExecute(conn, "CREATE TABLE Authorship(
  AuID INTEGER PRIMARY KEY AUTOINCREMENT,
  ArticleID INTEGER,
  AuthorID INTEGER,
  FOREIGN KEY (ArticleID) references Articles(ArticleID),
  FOREIGN KEY (AuthorID) references Authors(AuthorID))"
)

## parse xml file
xmlFile <- "pubmed-tfm-xml/pubmed22n0001-tf.xml"
dom <- xmlParse(xmlFile, validate=T)
root <- xmlRoot(dom)
n <- xmlSize(root)

## create internal data frames that will later be written to appropriate tables 
journal.df <- data.frame(JournalID = integer(),
                         ISSN = character(),
                         Title = character(),
                         ISSNType = character(),
                         CitedMedium = character(),
                         PubDate = character(),
                         ISOAbbreviation = character(),
                         stringsAsFactors = F)

article.df <-  data.frame(ArticleID = integer(),
                          ArticleTitle = character(),
                          JournalISSN = character(),
                          JournalName = character(),
                          JournalID = character(),
                          stringsAsFactors = F)

author.df <- data.frame(AuthorID = integer(),
                        LastName = character(),
                        ForeName = character(),
                        Initials = character(),
                        stringsAsFactors = F)

authorship.df <- data.frame(AuID = integer(),
                            ArticleID = integer(),
                            AuthorID = integer(),
                            stringsAsFactors = F)

article2.df <- data.frame(Num = integer(),
                          ID = integer(),
                          LN = character(),
                          FN = character(),
                          IN = character(),
                          stringsAsFactors = F)

## insert attributes into journals and articles internal data frames. 
## took into account that some journals did not have ISSN which affected
## the index where certain attributes would be found. 
for (i in 1:n) {
  journal.df[i, 1] <- i
  article.df[i, 1] <- i
  article.df[i, 2] <- xmlValue(root[[i]][[1]][[2]])
  #article.df[i, 3] <- i
  issnNode <- xmlName(root[[i]][[1]][[1]][[1]])
  if (issnNode == "ISSN") { 
    issn <- xmlValue(root[[i]][[1]][[1]][[1]])
    issnType <- xmlAttrs(root[[i]][[1]][[1]][[1]])
    citedMedium <- xmlAttrs(root[[i]][[1]][[1]][[2]])
    title <- xmlValue(root[[i]][[1]][[1]][[3]])
    isoAbb <- xmlValue(root[[1]][[1]][[1]][[4]])
  }
  else {
    issn <- ""
    issnType <- ""
    citedMedium <- xmlAttrs(root[[i]][[1]][[1]][[1]])
    title <- xmlValue(root[[i]][[1]][[1]][[2]])
    isoAbb <- xmlValue(root[[1]][[1]][[1]][[3]])
  }
  journal.df[i, 2] <- issn
  article.df[i, 3] <- issn
  journal.df[i, 3] <- title
  article.df[i, 4] <- title
  journal.df[i, 4] <- issnType
  journal.df[i, 5] <- citedMedium
  journal.df[i, 7] <- isoAbb
}

## filled in last name, forename and initials information 
count <- 0
for (i in 1:n) {
  node <- xmlValue(root[[i]][[1]][[3]])
  if (!is.na(node)) {
    size <- xmlSize(root[[i]][[1]][[3]])
    if (size > 0) {
      for (j in 1:size) {
        count <- count + 1
        author.df[count, 1] <- count
        attSize <- xmlSize(root[[i]][[1]][[3]][[j]])
        for (k in 1:attSize) {
          node <- xmlName(root[[i]][[1]][[3]][[j]][[k]])
          if (node == "LastName") {
            author.df[count, 2] <- xmlValue(root[[i]][[1]][[3]][[j]][[k]])
            article2.df[count, 3] <- xmlValue(root[[i]][[1]][[3]][[j]][[k]])
          } else if (node == "ForeName") {
            author.df[count, 3] <- xmlValue(root[[i]][[1]][[3]][[j]][[k]])
            article2.df[count, 4] <- xmlValue(root[[i]][[1]][[3]][[j]][[k]])
          } else {
            author.df[count, 4] <- xmlValue(root[[i]][[1]][[3]][[j]][[k]])
            article2.df[count, 5] <- xmlValue(root[[i]][[1]][[3]][[j]][[k]])
          }
        }
      }
    }
  }
}

## filled in information about PubDate. if multiple elements in PubDate,
## I added a dash between them so it would be in proper date format
## (i.e 1975-Oct-27)
for (i in 1:n) {
  node <- xmlName(root[[i]][[1]][[1]][[1]])
  if (node == "ISSN") {
    j <- 1
    newNode <- xmlName(root[[i]][[1]][[1]][[2]][[j]])
    while (newNode != "PubDate") {
      j <- j + 1
      newNode <- xmlName(root[[i]][[1]][[1]][[2]][[j]])
    }
    size <- xmlSize(root[[i]][[1]][[1]][[2]][[j]])
    if (size == 1) {
      journal.df[i, 6] <- xmlValue(root[[i]][[1]][[1]][[2]][[j]][[1]])
    } else {
      date <- xmlValue(root[[i]][[1]][[1]][[2]][[j]][[1]])
      for (k in 2:size) {
        date <- paste(date, xmlValue(root[[i]][[1]][[1]][[2]][[j]][[k]]), sep = '-')
      }
      journal.df[i, 6] <- date
    }
  } else {
    j <- 1
    newNode <- xmlName(root[[i]][[1]][[1]][[1]][[j]])
    while (newNode != "PubDate") {
      j <- j + 1
      newNode <- xmlName(root[[i]][[1]][[1]][[1]][[j]])
    }
    size <- xmlSize(root[[i]][[1]][[1]][[1]][[j]])
    if (size == 1) {
      journal.df[i, 6] <- xmlValue(root[[i]][[1]][[1]][[1]][[j]][[1]])
    } else {
      date <- xmlValue(root[[i]][[1]][[1]][[1]][[j]][[1]])
      for (k in 2:size) {
        date <- paste(date, xmlValue(root[[i]][[1]][[1]][[1]][[j]][[k]]), sep = '-')
      }
      journal.df[i, 6] <- date
    }
  }
}

## removed journals that have same ISSN and title because we don't want
## duplicate journals 
journal.df <- journal.df[!duplicated(journal.df[2:3]),]
journal.df <- tibble::rowid_to_column(data.frame(journal.df), "JournalId")

journalRows <- nrow(journal.df)

## fill in info about which journal corresponds to particular article
for (i in 1:n) {
  for (j in 1:journalRows) {
    if (article.df[i, 3] == journal.df[j, 3] & article.df[i, 4] == journal.df[j, 4]) {
      article.df[i, 5] <- j
      break
    }
  }
}

## write internal dataframes to tables
dbWriteTable(conn, "Journals", journal.df[, -c(2)], append=TRUE)
dbWriteTable(conn, "Articles", article.df[, -c(3:4)], append=TRUE)

## removed duplicate authors, those that have the same last name, forename and 
## initials and then write to table 
author.df <- author.df[!duplicated(author.df[2:4]),]

author.df <- tibble::rowid_to_column(data.frame(author.df), "AuthorId")
dbWriteTable(conn, "Authors", author.df[, -c(2)], append=TRUE)

articlerow <- nrow(article.df)

## article2 internal data frame shows the last name, forename and initials
## of the authors for each article. it includes redundancies in authors. 
authorshipCount <- 0
for (i in 1:articlerow) {
  numAuthors <- xmlSize(root[[i]][[1]][[3]])
  if (numAuthors > 0) {
    for (k in 1:numAuthors) {
      authorshipCount <- authorshipCount + 1
      article2.df[authorshipCount, 1] <- authorshipCount
      article2.df[authorshipCount, 2] <- i
    }
  }
}

article2rows <- nrow(article2.df)

## any N/A values filled with empty string 
for (i in 1:article2rows) {
  if (is.na(article2.df$LN[i])) {
    article2.df$LN[i] = ""
  }
  if (is.na(article2.df$FN[i])) {
    article2.df$FN[i] = ""
  }
  if (is.na(article2.df$IN[i])) {
    article2.df$IN[i] = ""
  }
}

authorrows <- nrow(author.df)

## go through each author in author data frame (which doesn't contain duplicates) 
## and find which articles they wrote by using the which statement which gives 
## you all the indexes in article2 data frame that contain that particular 
## author's last name, forename and initials combination
count <- 0
for (i in 1:authorrows) {
  if (is.na(author.df$LastName[i])) {
    author.df$LastName[i] = ""
  }
  if (is.na(author.df$ForeName[i])) {
    author.df$ForeName[i] = ""
  }
  if (is.na(author.df$Initials[i])) {
    author.df$Initials[i] = ""
  }
  index <- which(author.df$LastName[i] == article2.df$LN & author.df$ForeName[i] == article2.df$FN & author.df$Initials[i] == article2.df$IN)
  for (j in 1:length(index)) {
    count <- count + 1
    authorship.df[count, 1] <- count
    authorship.df[count, 2] <- article2.df[index[j], 2]
    authorship.df[count, 3] <- i
  }
}

## write data frame to table 
dbWriteTable(conn, "Authorship", authorship.df, append=TRUE)

## queries we were testing to make sure everything worked properly
dbGetQuery(conn, "SELECT COUNT(*) FROM Journals")
dbGetQuery(conn, "SELECT COUNT(*) FROM Authors")
dbGetQuery(conn, "SELECT COUNT(*) FROM Articles")
dbGetQuery(conn, "SELECT COUNT(*) FROM Authorship")
dbGetQuery(conn, "SELECT COUNT(*) FROM Articles where JournalID=1")
dbGetQuery(conn, "SELECT COUNT(*) FROM Articles where JournalID=2")
dbGetQuery(conn, "SELECT COUNT(*) FROM Articles where JournalID=3")
dbGetQuery(conn, "SELECT COUNT(*) FROM Articles where JournalID=4")
