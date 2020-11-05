# Read data from wiki output and extract the links
from pathlib import Path
import json
from tqdm import tqdm
import urllib

# Read Data and extract json
# Due to the limit of memory in reading, the whole dicts list still keeps its structure in 16 parts
data_dicts = []
data_Path = Path('output')
out_Path = Path('output_json')
json_load_problem_cnt = 0
for i in range(0, 17):  # Q-16
    data_dicts = []
    dataPath = Path(data_Path, 'A'+chr(ord('A')+i))
    for j in range(0, 100):
        datapath = Path(dataPath, 'wiki_%02d' % j)
        # Locate the end of the json manually
        try:
            with open(datapath, 'r', encoding='utf-8') as load_f:
                data_str = ""
                for line in load_f:
                    data_str += line.strip('\n')
                beg = 0
                pos = data_str.find('"}', beg)
                while pos != -1:
                    # Try twice. If it's still a mismatch, discard it
                    try:
                        data_dict = json.loads(data_str[beg:pos+2])
                        data_dicts.append(data_dict)
                    except:
                        try:
                            pos = data_str.find('"}', pos+2)
                            data_dict = json.loads(data_str[beg:pos+2])
                            data_dicts.append(data_dict)
                        except:
                            json_load_problem_cnt += 1
                            print("json_load problem num %d in" %
                                  json_load_problem_cnt, datapath)
                            pass
                    beg = pos+2
                    pos = data_str.find('"}', beg)
        except IOError:
            print("Files end")
            break
    
    # Build the dicts. Just record outlinks here
    for data_dict in data_dicts:
        text = data_dict['text']
        outlinks = []
        beg = 0
        # Locate the links manually
        pos = text.find('<a href=\"', beg)
        while pos != -1:
            end = text.find('\"', pos+9)
            outlinks.append(urllib.parse.unquote(text[pos+9:end]))
            beg = end+2
            pos = text.find('<a href=\"', beg)
        data_dict['outlinks'] = outlinks
        data_dict['inlinks'] = []
        data_dict['inlinks_id'] = []
        del data_dict['text']
        del data_dict['url']

    # Dump the data
    outPath = Path(out_Path, 'A'+chr(ord('A')+i)+'.json')
    with open(outPath, 'w', encoding='utf-8') as dump_f:
        json.dump(data_dicts, dump_f)
        print("Dump Done")
