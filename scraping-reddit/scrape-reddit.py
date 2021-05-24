#Import needed libraries
import praw
import pandas as pd
import praw.models
from praw.models import MoreComments
from datetime import datetime

#Setup Reddit API credentials
reddit = praw.Reddit(client_id='you client id', client_secret='your client secret', user_agent='your user agent')

url_prefix = 'https://www.reddit.com/r/' #define what subreddit that should be scraped
#Below is a list of parameters to be scraped. Consult the PRAW documentation for all possible parameters
comm_list = []
header_list = []
thread_author_list = []
author_list = []
subr_list = []
comment_score_list = []
thread_score_list = []
comment_url_list = []
rply_comment_author_list = []
comment_id_list = []
comment_parent_id_list = []
thread_url_list = []
score_ratio_list = []
thread_date_list = []
comment_date_list = []
comment_num_list = []
thread_id_list = []
thread_author_post_karma_list = []
thread_author_comment_karma_list = []
comment_author_post_karma_list = []
comment_author_comment_karma_list = []
thread_count = 0
backup_count = 1
# Change limit to limit the amount of threads. Change sort to change how the results are sorted, for instance by amount of comments og by relevance
for submission in reddit.subreddit('all').search("vertical farming", sort="relevance", limit=None):
    # Change limit to limit the depth of comments. Use None to remove all limits.
    submission.comments.replace_more(limit=5)
    thread_count += 1
    if submission.num_comments > 0:
        print('Nr. of threads scraped:', thread_count)
        print('Backup count: ', backup_count) #Used for the optional backup function
        for comment in submission.comments.list():
            header_list.append(submission.title)
            thread_author_list.append(submission.author)
            comm_list.append(comment.body)
            author_list.append(comment.author)
            comment_score_list.append(comment.score)
            thread_score_list.append(submission.score)
            subr_list.append(submission.subreddit)
            comment_url_list.append(comment.permalink)
            rply_comment_author_list.append('no_parent')
            comment_id_list.append(comment.id)
            comment_parent_id_list.append('no_parent')
            thread_url_list.append(submission.permalink)
            score_ratio_list.append(submission.upvote_ratio)
            thread_date_list.append(submission.created_utc)
            comment_date_list.append(comment.created_utc)
            comment_num_list.append(submission.num_comments)
            thread_id_list.append(submission.id)
            thread_author_post_karma_list.append(submission.author.link_karma)
            thread_author_comment_karma_list.append(submission.author.comment_karma)
            if hasattr(comment.author,'link_karma'):
                comment_author_post_karma_list.append(comment.author.link_karma)
            else:
                comment_author_post_karma_list.append('no_karma')
            if hasattr(comment.author,'comment_karma'):
                comment_author_comment_karma_list.append(comment.author.comment_karma)
            else:
                comment_author_comment_karma_list.append('no_karma')
            t = []
            t.extend(comment.replies)
            while t:
                header_list.append(submission.title)
                thread_author_list.append(submission.author)
                reply = t.pop(0)
                comm_list.append(reply.body)
                author_list.append(reply.author)
                comment_score_list.append(reply.score)
                thread_score_list.append(submission.score)
                subr_list.append(submission.subreddit)
                comment_url_list.append(comment.permalink)
                rply_comment_author_list.append(reply.parent().author)
                comment_id_list.append(comment.id)
                comment_parent_id_list.append(reply.parent_id)
                thread_url_list.append(submission.permalink)
                score_ratio_list.append(submission.upvote_ratio)
                thread_date_list.append(submission.created_utc)
                comment_date_list.append(reply.created_utc)
                comment_num_list.append(submission.num_comments)
                thread_id_list.append(submission.id)
                thread_author_post_karma_list.append(submission.author.link_karma)
                thread_author_comment_karma_list.append(submission.author.comment_karma)                
                #if not reply.author is None and not reply.author.link_karma is None and not reply.author.comment_karma is None:
                if hasattr(reply.author,'link_karma'):
                    comment_author_post_karma_list.append(reply.author.link_karma)
                else:
                    comment_author_post_karma_list.append('no_karma')
                if hasattr(reply.author,'comment_karma'):
                    comment_author_comment_karma_list.append(reply.author.comment_karma)
                else:
                    comment_author_comment_karma_list.append('no_karma')
        #Following is a crude backup function. It is optional but useful if scraping a large amount of posts and comments.
        if backup_count <= 3:
            backup_count += 1
            df = pd.DataFrame(header_list)
            df['thread_id_list'] = thread_id_list
            df['thread_url_list'] = thread_url_list
            df['thread_date_list'] = thread_date_list
            df['thread_author_list'] = thread_author_list
            df['thread_author_post_karma_list'] = thread_author_post_karma_list
            df['thread_author_comment_karma_list'] = thread_author_comment_karma_list
            df['thread_score_list'] = thread_score_list
            df['score_ratio_list'] = score_ratio_list
            df['subr_list'] = subr_list
            df['comment_num_list'] = comment_num_list
            df['comm_list'] = comm_list
            df['comment_id_list'] = comment_id_list
            df['author_list'] = author_list
            df['comment_author_post_karma_list'] = comment_author_post_karma_list
            df['comment_author_comment_karma_list'] = comment_author_comment_karma_list
            df['comment_score_list'] = comment_score_list
            df['rply_comment_author_list'] = rply_comment_author_list
            df['comment_parent_id_list'] = comment_parent_id_list
            df['comment_url_list'] = comment_url_list
            df['comment_date_list'] = comment_date_list
            df.columns = ['thread', 'thread_id', 'thread_url', 'thread_date', 'thread_author', 'thread_author_post_karma', 'thread_author_comment_karma', 'thread_score', 'score_ratio', 'subreddit', 'num_comments', 'comments', 'comment_id', 'comment_author', 'comment_author_post_karma', 'comment_author_comment_karma', 'comment_score', 'comment_parent', 'comment_parent_id', 'comment_url', 'comment_date']
            df['comments'] = df['comments'].apply(lambda x : x.replace('\n',''))
            df['thread_url'] = df['thread_url'].apply(lambda x : x.replace('/r/',url_prefix))
            df['comment_url'] = df['comment_url'].apply(lambda x : x.replace('/r/',url_prefix))
            df['thread_date'] = df['thread_date'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%d-%m-%Y %H:%M:%S'))
            df['comment_date'] = df['comment_date'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%d-%m-%Y %H:%M:%S'))
            df.to_csv('reddit.csv',index = False, encoding='utf-8')
        else:
            backup_count = 0
            print('Creating backup...')
            df = pd.DataFrame(header_list)
            df['thread_id_list'] = thread_id_list
            df['thread_url_list'] = thread_url_list
            df['thread_date_list'] = thread_date_list
            df['thread_author_list'] = thread_author_list
            df['thread_author_post_karma_list'] = thread_author_post_karma_list
            df['thread_author_comment_karma_list'] = thread_author_comment_karma_list
            df['thread_score_list'] = thread_score_list
            df['score_ratio_list'] = score_ratio_list
            df['subr_list'] = subr_list
            df['comment_num_list'] = comment_num_list
            df['comm_list'] = comm_list
            df['comment_id_list'] = comment_id_list
            df['author_list'] = author_list
            df['comment_author_post_karma_list'] = comment_author_post_karma_list
            df['comment_author_comment_karma_list'] = comment_author_comment_karma_list
            df['comment_score_list'] = comment_score_list
            df['rply_comment_author_list'] = rply_comment_author_list
            df['comment_parent_id_list'] = comment_parent_id_list
            df['comment_url_list'] = comment_url_list
            df['comment_date_list'] = comment_date_list
            df.columns = ['thread', 'thread_id', 'thread_url', 'thread_date', 'thread_author', 'thread_author_post_karma', 'thread_author_comment_karma', 'thread_score', 'score_ratio', 'subreddit', 'num_comments', 'comments', 'comment_id', 'comment_author', 'comment_author_post_karma', 'comment_author_comment_karma', 'comment_score', 'comment_parent', 'comment_parent_id', 'comment_url', 'comment_date']
            df['comments'] = df['comments'].apply(lambda x : x.replace('\n',''))
            df['thread_url'] = df['thread_url'].apply(lambda x : x.replace('/r/',url_prefix))
            df['comment_url'] = df['comment_url'].apply(lambda x : x.replace('/r/',url_prefix))
            df['thread_date'] = df['thread_date'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%d-%m-%Y %H:%M:%S'))
            df['comment_date'] = df['comment_date'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%d-%m-%Y %H:%M:%S'))
            df.to_csv('reddit.csv',index = False, encoding='utf-8')
    else:
        print('Thread nr.' ,thread_count,' - Has no comments')