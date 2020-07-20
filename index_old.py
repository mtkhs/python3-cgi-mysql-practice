#!/usr/bin/env python3
# coding: utf-8

import sys
import io
sys.stdout = io.TextIOWrapper( sys.stdout.buffer, encoding='utf-8' )

import cgi
form_data = cgi.FieldStorage( keep_blank_values = True )

import cgitb
cgitb.enable()

import textwrap
import datetime
import urllib

import os
from pathlib import Path
env_path = Path('.') / '.env'
from dotenv import load_dotenv
load_dotenv( dotenv_path = env_path, verbose = True )

import MySQLdb
con = None
cur = None

def print_http_headers():
    print( 'Content-Type: text/html; charset=utf-8' )
    print( '' )

def print_html():
    print( '<!DOCTYPE html>\n<html>' )
    
    print_html_head()
    print_html_body()
    
    print( '</html>' )

def print_html_head():
    source = textwrap.dedent( '''
        <head>
            <meta charset="UTF-8">
        </head>
    ''' )
    print( source )

def print_html_body():
    print( '''
    <body>
    ''' )
    print_form()
    print( '<hr>' )
    print_posts()
    print( '''
    </body>
    ''' )

def print_form():
    form_text = textwrap.dedent( '''
        <p>
        ひとこと掲示板
        </p>
        <form action="" method="POST">
            <input type="hidden" name="method" value="post">
            <input name="poster_name" value="" placeholder="なまえ">
            <br>
            <textarea name="body_text" value="" placeholder="本文"></textarea>
            <input type="submit" value="投稿">
        </form>
    ''' )
    print( form_text )

def print_posts():
    sql = "select * from posts"
    cur.execute( sql )

    rows = cur.fetchall()

    for row in rows:
        source = textwrap.dedent( '''
            <div class="meta">
                <span class="id">{post_id}</span>
                <span class="name">{poster_name}</span>
                <span class="date">{post_date}</span>
                <span class="delete">
                    <form method="post" action="" style="display: inline">
                        <input type="hidden" name="method" value="delete">
                        <input type="hidden" name="delete_id" value="{delete_id}">
                        <input type="submit" value="削除">
                    </form>
                </span>
            </div>
            <div class="message">
                <span>{post_body}</span>
            </div>
        ''' ).format( post_id = row[ 'id' ],
                poster_name = row[ 'name' ],
                post_date = row[ 'created_at' ],
                delete_id = row[ 'id' ],
                post_body = row[ 'body' ]
            )
        print( source )

def proceed_methods():
    method = form_data[ 'method' ].value
    if( method == 'post' ):
        poster_name = form_data[ 'poster_name' ].value
        body_text = form_data[ 'body_text' ].value

        sql = 'insert into posts ( name, body ) values ( %s, %s )'
        cur.execute( sql, ( poster_name, body_text ) )
        con.commit()

    elif( method == 'delete' ):
        delete_id = form_data[ 'delete_id' ].value

        sql = 'delete from posts where id=%s'
        cur.execute( sql, ( delete_id, ) )
        con.commit()

    source = textwrap.dedent( '''
        <html>
            <head>
                <meta http-equiv="refresh" content="3; url=./">
            </head>
            <body>
                処理が成功しました。3秒後に元のページに戻ります。
            </body>
        </html>
    ''' )
    print( source )

def main():
    print_http_headers()

    global con, cur
    con = MySQLdb.connect(
        host = os.environ.get( 'bbs_db_host' ),
        user = os.environ.get( 'bbs_db_user' ),
        passwd = os.environ.get( 'bbs_db_pass' ),
        db = os.environ.get( 'bbs_db_name' ),
        use_unicode = True,
        charset = 'utf8'
    )
    cur = con.cursor( MySQLdb.cursors.DictCursor )

    if( 'method' in form_data ):
        proceed_methods()
    else:
        print_html()

    cur.close()
    con.close()

if __name__ == "__main__":
    main()

