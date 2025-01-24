import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import matplotlib.pyplot as plt
import japanize_matplotlib


class PrefectureTouristSpotScraper:
    def __init__(self):
        self.base_url = "https://www.jalan.net"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 都道府県リスト
        self.prefectures = {
            'Hokkaido': '/kankou/010000/?screenId=OUW1021/',
            'Aomori': '/kankou/020000/?screenId=OUW1021',
            'Iwate': '/kankou/030000/?screenId=OUW1021',
            'Miyagi': '/kankou/040000/?screenId=OUW1021',
            'Akita': '/kankou/050000/?screenId=OUW1021',
            'Yamagata': '/kankou/060000/?screenId=OUW1021',
            'Fukushima': '/kankou/070000/?screenId=OUW1021',
            'Ibaraki': '/kankou/080000/?screenId=OUW1021',
            'Tochigi': '/kankou/090000/?screenId=OUW1021',
            'Gunma': '/kankou/100000/?screenId=OUW1021',
            'Saitama': '/kankou/110000/?screenId=OUW1021',
            'Chiba': '/kankou/120000/?screenId=OUW1021',
            'Tokyo': '/kankou/130000/?screenId=OUW1021',
            'Kanagawa': '/kankou/140000/?screenId=OUW1021',
            'Niigata': '/kankou/150000/?screenId=OUW1021',
            'Toyama': '/kankou/160000/?screenId=OUW1021',
            'Ishikawa': '/kankou/170000/?screenId=OUW1021',
            'Fukui': '/kankou/180000/?screenId=OUW1021',
            'Yamanashi': '/kankou/190000/?screenId=OUW1021',
            'Nagano': '/kankou/200000/?screenId=OUW1021',
            'Gifu': '/kankou/210000/?screenId=OUW1021',
            'Shizuoka': '/kankou/220000/?screenId=OUW1021',
            'Aichi': '/kankou/230000/?screenId=OUW1021',
            'Mie': '/kankou/240000/?screenId=OUW1021',
            'Shiga': '/kankou/250000/?screenId=OUW1021',
            'Kyoto': '/kankou/260000/?screenId=OUW1021',
            'Osaka': '/kankou/270000/?screenId=OUW1021',
            'Hyogo': '/kankou/280000/?screenId=OUW1021',
            'Nara': '/kankou/290000/?screenId=OUW1021',
            'Wakayama': '/kankou/300000/?screenId=OUW1021',
            'Tottori': '/kankou/310000/?screenId=OUW1021',
            'Shimane': '/kankou/320000/?screenId=OUW1021',
            'Okayama': '/kankou/330000/?screenId=OUW1021',
            'Hiroshima': '/kankou/340000/?screenId=OUW1021',
            'Yamaguchi': '/kankou/350000/?screenId=OUW1021',
            'Tokushima': '/kankou/360000/?screenId=OUW1021',
            'Kagawa': '/kankou/370000/?screenId=OUW1021',
            'Ehime': '/kankou/380000/?screenId=OUW1021',
            'Kochi': '/kankou/390000/?screenId=OUW1021',
            'Fukuoka': '/kankou/400000/?screenId=OUW1021',
            'Saga': '/kankou/410000/?screenId=OUW1021',
            'Nagasaki': '/kankou/420000/?screenId=OUW1021',
            'Kumamoto': '/kankou/430000/?screenId=OUW1021',
            'Oita': '/kankou/440000/?screenId=OUW1021',
            'Miyazaki': '/kankou/450000/?screenId=OUW1021',
            'Kagoshima': '/kankou/460000/?screenId=OUW1021',
            'Okinawa': '/kankou/470000/?screenId=OUW1021'
        }

    def get_tourist_spots(self, prefecture, path):
        """指定された都道府県の観光スポット情報と評価を取得（全件）"""
        spots_data = []
        
        try:
            search_url = f"{self.base_url}{path}"
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 観光スポットのリストを取得
            spot_elements = soup.select('div.item-listContents')
            
            # 全ての観光スポットを処理
            for spot in spot_elements:
                try:
                    # スポット名の取得
                    name_element = spot.select_one('div.item-name a')
                    spot_name = name_element.text.strip() if name_element else 'N/A'
                    spot_url = self.base_url + name_element['href'] if name_element and name_element.get('href') else 'N/A'
                    
                    # 説明文の取得
                    description = spot.select_one('div.item-description')
                    description_text = description.text.strip() if description else 'N/A'
                    
                    # カテゴリの取得
                    category = spot.select_one('div.item-category')
                    category_text = category.text.strip() if category else 'N/A'
                    
                    # 評価の取得
                    rating_element = spot.select_one('div.rating span.reviewPoint')
                    rating = float(rating_element.text) if rating_element else 0.0
                    
                    spot_data = {
                        '都道府県': prefecture,
                        'スポット名': spot_name,
                        'カテゴリ': category_text,
                        '説明': description_text,
                        'URL': spot_url,
                        '評価': rating
                    }
                    spots_data.append(spot_data)
                    
                except Exception as e:
                    print(f"スポットデータの解析エラー ({prefecture}): {e}")
                    continue
            
            print(f"{prefecture}: {len(spots_data)}件のスポットを取得")
            time.sleep(random.uniform(1, 2))
            
        except requests.exceptions.RequestException as e:
            print(f"リクエストエラー ({prefecture}): {e}")
        except Exception as e:
            print(f"予期せぬエラー ({prefecture}): {e}")
            
        return spots_data

    def scrape_all_spots(self):
        """全都道府県の観光スポット情報を取得（各全件）"""
        all_spots_data = []
        
        for prefecture, path in self.prefectures.items():
            print(f"\n{prefecture}の観光スポット情報を取得中...")
            spots_data = self.get_tourist_spots(prefecture, path)
            all_spots_data.extend(spots_data)
        
        if all_spots_data:
            df = pd.DataFrame(all_spots_data)
            current_date = datetime.now().strftime('%Y%m%d')
            filename = f'prefecture_tourist_spots_{current_date}.csv'
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            print(f"\n処理完了: {filename}に保存されました")
            return df
        else:
            print("\nデータを取得できませんでした")
            return pd.DataFrame()

    def display_summary(self, df):
        """取得したデータの要約を表示"""
        if not df.empty:
            print("\n=== データ収集サマリー ===")
            print(f"総スポット数: {len(df)}")
            print("\n都道府県別スポット数:")
            print(df['都道府県'].value_counts())
            print("\nカテゴリ別スポット数:")
            print(df['カテゴリ'].value_counts().head())
            
            # 都道府県ごとの評価の平均点を計算
            prefecture_ratings = df.groupby('都道府県')['評価'].mean().reset_index()
            prefecture_ratings = prefecture_ratings.rename(columns={'評価': '平均評価'})
            
            print("\n都道府県別の平均評価:")
            print(prefecture_ratings)
            
            return prefecture_ratings

def main():
    scraper = PrefectureTouristSpotScraper()
    print("全国の観光スポット情報の収集を開始します（各都道府県全件）...")
    spots_df = scraper.scrape_all_spots()
    
    if not spots_df.empty:
        prefecture_ratings = scraper.display_summary(spots_df)
        
        # 棒グラフを作成
        plt.figure(figsize=(12, 6))
        plt.bar(prefecture_ratings['都道府県'], prefecture_ratings['平均評価'])
        plt.xlabel('都道府県', fontsize=12)
        plt.ylabel('平均評価', fontsize=12)
        plt.xticks(rotation=90)
        plt.title('都道府県別の観光スポット平均評価', fontsize=14)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()