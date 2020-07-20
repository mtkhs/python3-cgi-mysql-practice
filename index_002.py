#!/usr/bin/env python3
# coding: utf-8

# print の出力時に日本語でもエラーが出ないようにするおまじない
import sys
import io
sys.stdout = io.TextIOWrapper( sys.stdout.buffer, encoding='utf-8' )

# CGIとして実行した際のフォーム情報を取り出すライブラリ
import cgi
form_data = cgi.FieldStorage( keep_blank_values = True )

# MySQLデータベース接続用ライブラリ
import MySQLdb
con = None
cur = None

# トップ画面のHTMLを出力するメソッド
def print_html():
    # html 開始
    print( '<!DOCTYPE html>' )
    print( '<html>' )

    # head 出力
    print( '<head>' )
    print( '<meta charset="UTF-8">' )
    print( '</head>' )

    # body 開始
    print( '<body>' )
    print( '<p>ひとこと掲示板</p>' )

    # 書き込みフォームを出力
    print( '<form action="" method="POST">' )
    print( '<input type="hidden" name="method_type" value="tweet">' )
    print( '<input type="text" name="poster_name" value="" placeholder="なまえ">' )
    print( '<br>' )
    print( '<textarea name="body_text" value="" placeholder="本文"></textarea>' )
    print( '<input type="submit" value="投稿">' )
    print( '</form>' )

    # 罫線を出力
    print( '<hr>' )

    # 書き込みの一覧を取得するSQL文を作成
    sql = "select * from posts"
    # SQLを実行
    cur.execute( sql )

    # 取得した書き込みの一覧の全レコードを取り出し
    rows = cur.fetchall()

    # 全レコードから1レコードずつ取り出すループ処理
    for row in rows:
        print( '<div class="meta">' )
        print( '<span class="id">' + row[ 'id' ] + '</span>' )
        print( '<span class="name">' + row[ 'name' ] + '</span>' )
        print( '<span class="date">' + row[ 'created_at' ] + '</span>' )
        print( '</div>' )
        print( '<div class="message"><span>' + row[ 'body' ] + '</span></div>' )

    # body 閉じ
    print( '</body>' )

    # html 閉じ
    print( '</html>' )

# フォーム経由のアクセスを処理するメソッド
def proceed_methods():
    # フォームの種類を取得（今のところ書き込みのみ）
    method = form_data[ 'method_type' ].value

    # tweet （書き込み） だったら
    if( method == 'tweet' ):
        # 名前を取り出し
        poster_name = form_data[ 'poster_name' ].value
        # 投稿内容を取り出し
        body_text = form_data[ 'body_text' ].value

        # 投稿をデータベースに書き込むSQL文を作成
        sql = 'insert into posts ( name, body ) values ( %s, %s )'
        # 取り出した名前と投稿内容をセットしてSQLを実行
        cur.execute( sql, ( poster_name, body_text ) )
        con.commit()

    # 処理に成功したらトップ画面に自動遷移するページを出力
    print( '<!DOCTYPE html>' )
    print( '<html>' )
    print( '    <head>' )
    print( '        <meta http-equiv="refresh" content="5; url=./">' )
    print( '    </head>' )
    print( '    <body>' )
    print( '        処理が成功しました。5秒後に元のページに戻ります。' )
    print( '    </body>' )
    print( '</html>' )

# メイン処理を実行するメソッド
def main():
    # CGIとして実行するためのおまじない
    print( 'Content-Type: text/html; charset=utf-8' )
    print( '' )

    # ここでデータベースに接続しておく
    global con, cur
    try:
        con = MySQLdb.connect(
            host = 'xxx.xxx.xxx.xxx',
            user = 'yourname',
            passwd = 'yourpassword',
            db = 'yourdbname',
            use_unicode = True,
            charset = 'utf8'
        )
    except MySQLdb.Error as e:
        print( 'データベース接続に失敗しました。' )
        print( e )
        # データベースに接続できなかった場合は、ここで処理を終了
        exit()

    cur = con.cursor( MySQLdb.cursors.DictCursor )

    # フォーム経由のアクセスかを判定
    if( 'method_type' in form_data ):
        # フォーム経由のアクセスである場合は、フォームの種類に従って処理を実行
        proceed_methods()
    else:
        # フォーム経由のアクセスでない場合は、通常のトップ画面を表示
        print_html()

    # 一通りの処理が完了したら最後にデータベースを切断しておく
    cur.close()
    con.close()

# Pythonスクリプトとして実行された場合のみ実行
if __name__ == "__main__":
    # main() を実行
    main()

