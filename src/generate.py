import os 
import json 

skip = ['src']

requiredFiles = ["__repo__.json"]

__repos__ = []

for path in os.listdir("../"):

    if os.path.isdir(f"../{path}"):
        if os.path.isfile(f'../{path}/readme.md'):
                os.remove(f'../{path}/readme.md')
        if requiredFiles == os.listdir(f"../{path}"):
            print(f'[ LOG ] Generating readme.md file for {path}')
            data = json.load(open(f'../{path}/__repo__.json','r',encoding="utf-8"))
            data['id'] = path
            template = open('./template.md').read()
            __repos__.append(data)
            
            # Replace placeholders:
            template = template.replace('{title}',data.get('name'))
            template = template.replace('{Repolink}',data.get('link').replace('@github','https://github.com').replace('@gitlab','https://gitlab.com'))
            template = template.replace('{authorName}',data.get('author').replace('@github/','').replace('@gitlab/',''))
            template = template.replace('{authorLink}',data.get('author').replace('@github','https://github.com').replace('@gitlab','https://gitlab.com'))
            template = template.replace('{status}',data.get('status'))
            template = template.replace('{description}',data.get('description'))
            template = template.replace('{types}',"\n".join([f"{type.get('title')} | {'✅' if type.get('postsComment') else '❌'}" for type in data.get('datamines')]))
            with open(f'../{path}/readme.md','a+',encoding="utf-8") as f:
                f.write(template)
            print(f'[ SUCCESS ] Generated readme.md file for {path}')



if os.path.isfile(f'../__repos__.json'):
    os.remove(f'../__repos__.json')

print("[ LOG ] Generating __repos__.json")    

with open(f'../__repos__.json','a+',encoding="utf-8") as f:
    f.write(json.dumps(__repos__))

print("[ SUCCESS ] Generated readme.md for all repository's")    
print("[ SUCCESS ] Generated __repos__.json")    

print("[ LOG ] Generating readme.md")

template = open('./readmeTemplate.md',encoding="utf-8").read()
owners = []
repos = []

for __repo__ in __repos__:
    Authorname = __repo__.get('author').replace('@github/','').replace('@gitlab/','')
    Authorlink = __repo__.get('author').replace('@github','https://github.com').replace('@gitlab','https://gitlab.com')
    RepoName = __repo__.get('name')
    RepoLink = __repo__.get('id')
    formattedAuthor = f"- [{Authorname}]({Authorlink})"
    formattedLink = f"- [{RepoName}](./{RepoLink})"
    if formattedAuthor not in owners:
        owners.append(formattedAuthor)
    if formattedLink not in repos:
        repos.append(formattedLink)
    


template = template.replace('{list}',"\n".join(repos))
template = template.replace('{owners}',"\n".join(owners))

if os.path.isfile(f'../readme.md'):
    os.remove(f'../readme.md')


with open(f'../readme.md','a+',encoding="utf-8") as f:
    f.write(template)

print('[ SUCCESS ] Generated readme.md')