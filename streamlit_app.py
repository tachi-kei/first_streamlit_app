# APIのインポート
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# タイトルを表示
streamlit.title('My Parents New Healthy Diner')
# ヘッダーを表示
streamlit.header('Breakfast Menu')
# メニューをテキストで表示
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# スムージーに入れたいフルーツを選択する
# AWSのS3に接続し、フルーツのデータを取得
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# フルーツを選択できるようにする
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# 選択したフルーツ一覧を表示
streamlit.dataframe(fruits_to_show)


# 政府のデータからフルーツの情報を参考にできるようにする
# get_fruityvice_data関数を定義
# リクエストパラメーターを送信
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# 一覧のタイトル表示
streamlit.header("Fruityvice Fruit Advice!")
try:
  # テキストボックスに入力された情報を変数に代入
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  # テキストボックスが空の場合エラーメッセージを表示
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  # テキストボックスに情報が入っている場合一覧を表示する
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

# 以下の処理を無効にする
streamlit.stop()

# snowflakeからデータを表示
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
# リストからフルーツを加えられるようにテキストボックスを作成
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)

#正しく動かない
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
