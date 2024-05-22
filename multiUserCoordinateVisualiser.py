import json
import matplotlib.pyplot as plt

# Load the JSON data from the file
with open('extractedDataTEST2.json', 'r') as f:
    all_data = json.load(f)

# Iterate over each user's data
for user_id, user_data in all_data['__collections__']['users'].items():
    coordinates = user_data['__collections__']['Journeys'][f'{user_id} Journey']['Coordinates']
    
    x_values = [coord['X'] for coord in coordinates]
    y_values = [coord['Y'] for coord in coordinates]

    plt.plot(x_values, y_values, linestyle='-', linewidth=0.5, label=f'User {user_id}')

plt.title('Plot of Journey Coordinates')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)

# Set x and y limits
plt.xlim(-191.5, 166.5)
plt.ylim(-98.5, 136.5)

plt.legend()

plt.show()
