import subprocess
import json
import matplotlib.pyplot as plt

node_script_path = '../helpers/csvTojson.js'

# Execute the Node.js script
jsonResult = subprocess.run(['node', node_script_path], capture_output=True, text=True)
jsonData = []

# Check the output and error
if jsonResult.returncode == 0:
    print('Node.js script executed successfully.')
    print('Output:', jsonResult.stdout)
    try:
        jsonData = json.loads(jsonResult.stdout)
    except json.JSONDecodeError as err:
        print("error while parsing json",err)
else:
    print('Error executing Node.js script.')
    print('Error:', jsonResult.stderr)

ages = [int(item["Age"]) for item in jsonData]
names = [item["Name"] for item in jsonData]
genders = [item["Gender"] for item in jsonData]

unique_genders = list(set(genders))
color_map = plt.get_cmap("tab20")  # Choose a color map
colors = [color_map(i) for i in range(len(unique_genders))]
gender_to_color = dict(zip(unique_genders, colors))
bar_colors = [gender_to_color[gender] for gender in genders]


plt.bar(names, ages, color = colors)
plt.xlabel("Name")
plt.ylabel("Age")
plt.title("Age Distribution")

handles = [plt.Rectangle((0, 0), 1, 1, color=gender_to_color[gender]) for gender in unique_genders]
labels = unique_genders
plt.legend(handles, labels, title="Gender")

plt.show()