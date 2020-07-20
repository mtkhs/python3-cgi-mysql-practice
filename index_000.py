#!/usr/bin/env python3
# coding: utf-8

# print の出力時に日本語でもエラーが出ないようにするおまじない
import sys
import io
sys.stdout = io.TextIOWrapper( sys.stdout.buffer, encoding='utf-8' )

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

    # body 閉じ
    print( '</body>' )

    # html 閉じ
    print( '</html>' )

# メイン処理を実行するメソッド
def main():
    # CGIとして実行するためのおまじない
    print( 'Content-Type: text/html; charset=utf-8' )
    print( '' )

    # トップ画面を表示
    print_html()

# Pythonスクリプトとして実行された場合のみ実行
if __name__ == "__main__":
    # main() を実行
    main()

