# -*- coding: utf-8 -*-

import pymysql

db = pymysql.connect(host="localhost", user="root", password="123456",database="music163", charset='utf8mb4')
cursor = db.cursor()

def save_album_info(album_info):
    '''
    保存专辑信息（专辑号、专辑名、歌手号、歌手名、发行时间、发行单位）到数据表album_info
    '''
    sql = """
        INSERT INTO album_info 
        (album_id, album_name, singer_id, singer_name, release_time, release_company)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    try:
        cursor.execute(sql, (album_info['album_id'], album_info['album_name'], album_info['singer_id'], album_info['singer_name'], album_info['release_time'], album_info['release_company']))
        db.commit()
        
    except:
        db.rollback()
        
        
def save_songs_info(songs_info):
    '''
    保存歌曲信息（歌曲号、歌曲名、所属专辑号、所属专辑名）到数据表song_info
    '''
    sql = """
        INSERT INTO song_info
        (song_id, song_name, album_id, album_name)
        VALUES (%s, %s, %s, %s)
        """
    try:
        for song_info in songs_info:
            cursor.execute(sql,(song_info['song_id'], song_info['song_name'], song_info['album_id'], song_info['album_name']))
            db.commit()
    except:
        db.rollback()
        
def get_song_ids():
    '''
    查询song_info表中所有评论数为空的歌曲号，以列表的形式返回
    '''
    sql = """
        SELECT song_id FROM song_info WHERE comment_num IS NULL  
        """
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        song_ids = []
        for row in results:
            song_ids.append(row[0])
        return song_ids
    except:
        print('歌曲id获取失败')
        return None
    
def save_comment_num(comment_num, song_id):
    '''
    保存评论数到数据表song_info
    '''
    sql = """
        UPDATE song_info SET comment_num = %s WHERE song_id = %s
        """
    try:
        cursor.execute(sql,(comment_num, song_id))
        db.commit()
    except:
        db.rollback()
        

def close_db():
    '''
    关闭数据库
    '''
    db.close()
