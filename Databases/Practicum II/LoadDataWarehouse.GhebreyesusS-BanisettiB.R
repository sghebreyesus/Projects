
#install.packages("DBI")
#install.packages("RMySQL")
#install.packages("tinytex")

##Connect to Database

library(DBI)
library(RMySQL)
library(tinytex)
options("mysql.local_infile" = TRUE)
dbcon<-dbConnect(MySQL(),host="localhost",user="root",
                 password="Asm@rino123",port=3306)
dbSendQuery(dbcon, "CREATE DATABASE journal_star_db")
dbSendQuery(dbcon, "USE journal_star_db")
dbcon<-dbConnect(MySQL(),host="localhost",dbname="journal_star_db",user="root",
                 password="Asm@rino123",port=3306)
dbcon

##Create Database

dbExecute(dbcon,"DROP TABLE IF EXISTS f_journal")

dbExecute(dbcon,"DROP TABLE IF EXISTS d_time")

dbExecute(dbcon,"CREATE TABLE IF NOT EXISTS d_time(
  t_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  month varchar(64),
  year INTEGER, 
  quarter INTEGER)")

dbExecute(dbcon,"CREATE TABLE IF NOT EXISTS f_journal(
  journalID INTEGER PRIMARY KEY,
  title TEXT,
  t_id INTEGER NOT NULL REFERENCES d_time(t_id),
  num_of_articles INTEGER,
  num_of_authors INTEGER
)")

dbExecute(dbcon,"CREATE INDEX year_idx on d_time(year)")

dbExecute(dbcon,"CREATE INDEX yr_mth_idx on d_time(year,month)")

dbExecute(dbcon,"CREATE INDEX mth_idx on d_time(month)")

dbExecute(dbcon,"CREATE INDEX qtr_idx on d_time(quarter)")

dbFile = "Pubmed.db"
conn_lite <- dbConnect(RSQLite::SQLite(), dbFile)

journal_df = dbGetQuery(conn_lite, "SELECT j.JournalID,j.title,j.PubDate,
                            count(distinct(art.ArticleID)) as num_of_arts,
                            count(distinct(auth.AuthorID)) as num_of_authors
                            FROM Journals AS j
                            JOIN Articles AS art 
                            JOIN Authorship auth
                            ON j.JournalID = art.JournalID
                            AND art.ArticleID = auth.ArticleID
                            group by j.JournalID,j.title,j.PubDate")
nrow(journal_df)

head(journal_df,5)

library(stringr)
#replacing the Spring, Summer, Fall, Winter with respective months
journal_df$PubDate <- str_replace(journal_df$PubDate,'Spring','Mar')
journal_df$PubDate <- str_replace(journal_df$PubDate,'Summer','Jun')
journal_df$PubDate <- str_replace(journal_df$PubDate,'Fall','Sep')
journal_df$PubDate <- str_replace(journal_df$PubDate,'Winter','Dec')

#gsub('([0-9]{4}[-])([0-9]{4}$)','\\2','1768-1990')
journal_df$PubDate<-gsub('([0-9]{4}[-])([0-9]{4}$)','\\2',journal_df$PubDate)#2009-2019 to 2019

#1975 Jul-Aug 12
#gsub('([0-9]{4}[\x20])([a-zA-Z]{3}[-])([a-zA-Z]{3}[\x20][0-9]{1,2})','\\1\\3','1975 Jul-Aug 12') to 1975 Aug 12
journal_df$PubDate<-gsub('([0-9]{4}[\x20])([a-zA-Z]{3}[-])([a-zA-Z]{3}[\x20][0-9]{1,2})','\\1\\3',journal_df$PubDate)

#gsub('([0-9]{4}[\x20][a-zA-Z]{3}[\x20])([1-9]?[0-9][-])([0-9]?[0-9])','\\1\\3','1975 Aug 5-31')###1975 Aug 15-31 to 1975 Aug 31
journal_df$PubDate<-gsub('([0-9]{4}[\x20][a-zA-Z]{3}[\x20])([1-9]?[0-9][-])([0-9]?[0-9])','\\1\\3',journal_df$PubDate)

#gsub('([0-9]{4}[\x20])([a-zA-Z]{3}[\x20][1-9]?[0-9][-])([a-zA-Z]{3}[\x20][1-9]?[0-9])','\\1\\3','1976 Sep 30-Oct 2')### 1976 Sep 30-Oct 2 to 1976 Oct 2
journal_df$PubDate<-gsub('([0-9]{4}[\x20])([a-zA-Z]{3}[\x20][1-9]?[0-9][-])([a-zA-Z]{3}[\x20][1-9]?[0-9])','\\1\\3',journal_df$PubDate)### 1976 Sep 30-Oct 2

journal_df$PubDate<-gsub('([0-9]{4}[\x20])([a-zA-Z]{3})[-]([a-zA-Z]{3})','\\1\\3',journal_df$PubDate)#1988 Jun-Jul to 1988 Jul
#gsub('([0-9]{4}[\x20])([a-zA-Z]{3})[-]([a-zA-Z]{3})','\\1\\3','1987 Jul-Aug')#1988 Jun-Jul

#gsub('([0-9]{4}[\x20][a-zA-Z]{3}[-])([0-9]{4}[\x20][a-zA-Z]{3})','\\2','1975 Dec-1976 Jan')## 1975-1976 Jan to 1976 Jan
journal_df$PubDate<-gsub('([0-9]{4}[\x20][a-zA-Z]{3}[-])([0-9]{4}[\x20][a-zA-Z]{3})','\\2',journal_df$PubDate)## 1975-1976 Jan


populate_d_time_n_f_journal <- function() {
    for (i in 1:nrow(journal_df)){
        dt_field <- journal_df[i,'PubDate']
        dt_len <- nchar(dt_field)
        #print(paste(dt_field,dt_len))
        v_year <- NA
        v_month <- NA
        v_quarter <- NA
        month_flg<-0
        if (dt_len == 4){
            v_year = dt_field
        }
        else if (dt_len == 8 | dt_len == 10 | dt_len == 11){
            v_year = substr(dt_field,1,4)
            v_month = tolower(substr(dt_field,6,8))
            month_flg<-1
            if (v_month=='jan' | v_month =='feb' | v_month =='mar'){
                v_quarter = 1
            }
            else if (v_month=='apr' | v_month =='may' | v_month =='jun'){
                v_quarter = 2
            }
            else if (v_month=='jul' | v_month =='aug' | v_month =='sep'){
                v_quarter = 3
            }
            else{
                v_quarter = 4
            }
        }
        
        #insertion into dimension table d_time
        month_p <- ""
        # Retreiving time id (t_id)
        if (!is.null(v_month) & !is.na(v_month)){
            month_p<-paste0('"',v_month,'"')
            sqlCmd = paste0('select t_id from d_time where year=',v_year,
                            ' and month=',month_p)
        }
        else{
            sqlCmd = paste0('select t_id from d_time where year=',v_year,
                          ' and month is null')
        }
        #print(month_p)
        #print(sqlCmd)
        # Get SQL query result from the database
        v_t_id = dbGetQuery(dbcon, sqlCmd)
        v_t_id = v_t_id[1,1]
        #print(paste("tid is ",v_t_id))
        
        if (is.null(v_t_id) | is.na(v_t_id)){
            if (month_flg==1){
              stmt<-paste0('insert into d_time(year,month,quarter) 
                         values (',
                         v_year,',',
                         month_p,',',
                         v_quarter,')')
            }
            else{
              stmt<-paste0('insert into d_time(year) 
                         values (',
                         v_year,')')
            }
            #print(stmt)
            dbSendQuery(dbcon,stmt)
            v_t_id = dbGetQuery(dbcon, "select last_insert_id()")
            v_t_id = v_t_id[1,1]
            #print(paste("lastinsert: ",v_t_id))
        }
        
        # Retreiving journal id 
        sqlCmd = paste0('select journalID from f_journal where journalID=',
                        journal_df[i,'JournalID'])
        #print(sqlCmd)
        # Get SQL query result from the database
        v_j_id = dbGetQuery(dbcon, sqlCmd)
        v_j_id = v_j_id[1,1]
        #print(paste("journal id is ",v_j_id))
        
        if (is.null(v_j_id) | is.na(v_j_id)){   
            #insertion into fact table f_journal 
            title_p<-paste0('"',journal_df[i,'Title'],'"')
            stmt<-paste0('insert into f_journal(journalID,title,t_id,
                          num_of_articles,num_of_authors) 
                          values (',journal_df[i,'JournalID'],',',
                         title_p,',',
                         v_t_id,',',
                         journal_df[i,'num_of_arts'],',',
                         journal_df[i,'num_of_authors']
                         ,')')
            #print(stmt)
            dbSendQuery(dbcon,stmt)
        }    
    }    
}

populate_d_time_n_f_journal()
