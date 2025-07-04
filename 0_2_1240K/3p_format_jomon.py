#!/usr/bin/env python3
"""
FAMファイル処理スクリプト
指定された文字列の除去、置換、および行頭の0の置換を行います。
"""

import sys
import re

def process_fam_file(input_file, output_file):
    """
    FAMファイルを処理し、指定された変換を適用する
    
    Args:
        input_file: 入力ファイルのパス
        output_file: 出力ファイルのパス
    """
    
    # 除去する文字列のリスト
    remove_strings = [".DG", ".SG", "_o", "_brother.I13886", "_131464_B_noUDG", "_noUDG","_dup.JHM06", "_lc","_dup.JHM06"]
    
    # 行頭の0を置換するためのマッピング
    # 2番目のフィールドの先頭文字/文字列に基づいて判定
    prefix_mapping = {
        'T5': 'Todoroki',
        'T2': 'Todoroki2',
        'T3': 'Todoroki3',
        'Mabuni': 'Mabuni',
        'A7': 'IyaiA',
        'I': 'Iyai',
        'Iyai18b': 'Iyai18b',
        'F': 'Funadomari',
        'M3': 'Mitsusawa',
        'C': 'Chidorigakubo',
        'K': 'Katsuren',
        'B': 'Bugeido'
    }
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # 改行を除去
            line = line.rstrip('\n')
            
            # 空行の場合はスキップ
            if not line:
                continue
            
            # フィールドに分割
            fields = line.split()
            
            # 少なくとも2つのフィールドがあることを確認
            if len(fields) >= 2:
                # 行頭が0の場合の処理
                if fields[0] == '0':
                    second_field = fields[1]
                    
                    # prefix_mappingに基づいて置換
                    for prefix, replacement in prefix_mapping.items():
                        if second_field.startswith(prefix):
                            fields[0] = replacement
                            break
            
            # 行全体を再結合
            line = ' '.join(fields)
            
            # 文字列の除去
            for remove_str in remove_strings:
                line = line.replace(remove_str, '')
            
            # 特定の文字列置換
            # Japan_HG_Jomon -> Japan_Rokutsu_Jomon
            line = line.replace('Japan_HG_Jomon', 'Japan_Rokutsu_Jomon')
            line = line.replace('Nepal_Mustang_Chokhopani_IA', 'Chokupani')
            line = line.replace('Russia_Yana_UP', 'Yana_UP')
            line = line.replace('Russia_Ust_Ishim_HG', 'Ust_Ishim')
            line = line.replace('Russia_Ust_Ishim', 'Ust_Ishim')
            line = line.replace('Russia_Shamanka_Eneolithic', 'Shamanka_EN')
            line = line.replace('Russia_MA1_HG.SG', 'MA1')
            line = line.replace('Russia_KolymaRiver_LN', 'KolymaRiver')
            line = line.replace('Russia_DevilsCave_N', 'DevilsCave_N')
            # -9 -> 2
            line = line.replace('-9', '2')
            
            # Japan_Jomon IK002 -> Japan_Ikawazu_Jomon
            # スペースを含む置換なので、正規表現を使用
            line = re.sub(r'Japan_Jomon\s+IK002', r'Japan_Ikawazu_Jomon\s+IK002', line)
            
            # Japan_Jomon Sanganji -> Japan_Sanganji_Jomon
            line = re.sub(r'Japan_Jomon\s+Sanganji', r'Japan_Sanganji_Jomon\s+Sanganji', line)
            
            # Yondaedo_1 または Yondaedo_2 -> Yondaedo
            line = re.sub(r'Yondaedo_[12]', 'Yondaedo', line)
            
            # 処理済みの行を出力
            outfile.write(line + '\n')
    
    print(f"処理が完了しました。出力ファイル: {output_file}")

def main():
    """メイン関数"""
    # コマンドライン引数の処理
    if len(sys.argv) < 2:
        print("使用方法: python script.py <入力ファイル> [出力ファイル]")
        print("出力ファイルが指定されない場合は、入力ファイル名.processed が使用されます")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 出力ファイル名の決定
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # 入力ファイル名に .processed を追加
        output_file = input_file + '.processed'
    
    try:
        process_fam_file(input_file, output_file)
    except FileNotFoundError:
        print(f"エラー: ファイル '{input_file}' が見つかりません")
        sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()