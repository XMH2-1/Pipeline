import re


def get_df(text_file_path, cls_name):
  print(text_file_path)

  text_dict = {}

  f = open(text_file_path).read()
  f = ReplaceThreeOrMore(f)
  f = sent_tokenize(f)

  sent = [f[sent].replace('.', ' ').replace(' Г ', '').replace(' г ', '') for sent in range(1, len(f))]
  
  for label_sen in sent:
    if len(label_sen) > 200:
      
      label_sen = re.sub(r'[^а-яА-Я ]', ' ', label_sen)
      label_sen = label_sen.split()
      label_sen = " ".join(label_sen)

      text_dict.update({label_sen:cls_name})

  return text_dict


cls_dict = {'Договоры для акселератора/Договоры поставки':1,
            "Договоры для акселератора/Договоры оказания услуг":2,
            "Договоры для акселератора/Договоры подряда":3,
            "Договоры для акселератора/Договоры аренды":4,
            "Договоры для акселератора/Договоры купли-продажи":5}

file = '/content/classes.json'
with open(file) as train_file:
    dict_train = json.load(train_file)

train = pd.DataFrame.from_dict(dict_train, orient='index').reset_index()
train[0]= train[0].map(lambda x:cls_dict[x])
for i in range(len(train['index'])):
  text_recognition('/content/docs/'+train['index'].values[i], '/content/docs/'+str(train[0].values[i]))

files_labels = os.listdir('/content/labeled_classes')
df_dict = {}
for file_l in files_labels:
  cls_name = file_l[0]
  df_dict.update(get_df('/content/labeled_classes/'+file_l, cls_name))
