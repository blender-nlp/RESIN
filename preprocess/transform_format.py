from rsd2ltf import rsd2ltf, write2file

import json
import os

def transform_to_ldc(doc_dict, cluster_name, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "data", "source"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "data", "source", "ltf"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "data", "source", "mp4"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "data", "source", "ltf", "ltf"), exist_ok=True)

    tab_lines = []
    tab_example_line =  "test	V1.0	test	L0C04CW9J	https://www.diariocritico.com/noticia/123483/noticias/retiran-en-eeuu-productos-con-mantequilla-de-mani.html	.gif.ldcc	ce2004	n/a	spa	11	7ad8ac445ef45f050f6ce6f14a4047f3	ea03ca61cadb5542bac78b11991f20fe	2021-06-18	n/a	present".split('\t')

    article_num = 0
    for doc_id, doc_txt in doc_dict.items():
        ltf_root = rsd2ltf(doc_txt, doc_id, "nltk+linebreak", "nltk_wordpunct", False)
        write2file(ltf_root, os.path.join(output_dir, "data", "source", "ltf", "ltf", doc_id+".ltf.xml"))
        new_tab_line = tab_example_line.copy()
        new_tab_line[2] = new_tab_line[2] + '_' + str(article_num)
        new_tab_line[3] = doc_id
        new_tab_line[6] = cluster_name
        new_tab_line = "\t".join(new_tab_line)
        tab_lines.append(new_tab_line)
        article_num += 1
    
    os.makedirs(os.path.join(output_dir, "docs"), exist_ok=True)
    with open(os.path.join(output_dir, "docs", "parent_children.tab"), 'w', encoding='utf-8') as f:
        for line in tab_lines:
            f.write(line + '\n')


if __name__ == "__main__":
    # test_doc_dict = {"doc_1": "hello world!", "doc_2": "This is a test document cluster."}
    # test_name = "test_cluster"
    # output_dir = "test_data"
    # transform_to_ldc(test_doc_dict, test_name, output_dir)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str)
    parser.add_argument('--name', type=str, default="default")
    parser.add_argument('--output_dir', type=str, default="./example_data")
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        doc_dict = json.loads(f.read())
    
    transform_to_ldc(doc_dict, args.name, args.output_dir)
