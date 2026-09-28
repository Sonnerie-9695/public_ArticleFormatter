from pathlib import Path

input = "input/sample_01.md"
output = "output/sample_01.md"# テスト用。あとでディレクトリの中身を読んで逐次実行に変える

h2_candidates = ("## ","##　")
quote_candidates = (">")

def return_path(path:str) -> Path:
    return Path(path)


def process_all_lines(input_path:Path) -> list[str]:

    formatted_text = []
    quote_block = False
    blank_count = 0

    with open(input_path,mode="r",encoding="utf-8") as text:

        for raw_line in text:

            # line = raw_line.strip("\n")# 欲しいのは末尾の\n削除だけ
            line = raw_line.removesuffix("\n")

            if line == "":
                quote_block = False
                blank_count += 1
                continue
            
            else:
                if blank_count == 1:
                    formatted_text.append("")
                    
                for ct in range(0,blank_count // 2):# range(0,0)は長さゼロ。空行が1のときこのループは実行されない
                    formatted_text.append("<br>")

                blank_count = 0 # 空行カウントをゼロに戻す
            
            if line.startswith(quote_candidates):
                quote_block = True

            

            formatted_text.append(format_all(line,quote_block))

        if not blank_count == 0:
            formatted_text.append("")# 文末に改行を1つ足す（ループ処理内では文末の空行を処理できないので暫定措置）

    return formatted_text



def format_all(line:str,quote_block:bool=False)-> str:

    if quote_block:
        return format_quote_block(line)

    if line.startswith(h2_candidates):
        return format_h2(line)

    else:
        return line


def format_quote_block(line:str) -> str:

    quote = line.removeprefix(">").lstrip(" ")

    return "> " + quote


def format_h2(line:str) -> str:

    h2 = line.replace("　"," ",1)#はじめの1回の全角スペースだけ半角スペースに変換

    line_formatted = f"""
<br>
<br>
{h2}
<br>
<br>
"""

    return line_formatted



def save_formatted_text(target:Path,formatted_text:list[str]):
    content = "\n".join(formatted_text)
    # print(content)
    target.write_text(content,encoding="utf-8")


# def format_2_blank_2_br(blank_count:int) -> str | None:
#     if blank_count == 1:
#         return ""
        
#     for ct in range(0,blank_count // 2):# range(0,0)は長さゼロ。空行が1のときこのループは1度だけ実行される
#         return "<br>" #失敗

if __name__ == "__main__":
    input_path = return_path(input)
    output_path = return_path(output)
    formmatted_text =  process_all_lines(input_path)
    save_formatted_text(output_path,formmatted_text)
