import requests
import xml.etree.ElementTree as ET
import json

def fetch_courses():
    courses_dict = {}

    for page_num in range(0,400):
        # Construct the URL with the current page number
        url = f"https://mytimetable.mcmaster.ca/api/courses/suggestions?term=3202510&cams=MCMSTiOFF_MCMSTiMCMST_MCMSTiMHK_MCMSTiSNPOL_MCMSTiCON&course_add=%20&page_num={page_num}&sco=0&sio=1&already=&_=1723996118000"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve data for page {page_num}")
            break

        # Parse the XML response
        root = ET.fromstring(response.text)

        # Check if no courses are returned (i.e., courses="0")
        courses_count = int(root.text.strip())
        print(page_num, courses_count)
        if courses_count == 0:
            print(f"No more courses found at page {page_num}. Stopping.")
            break

        # Iterate through the results
        for course in root.findall(".//rs"):
            course_code = course.text.strip()
            course_info = course.get("info")
            courses_dict[course_code] = course_info
            print(f"{course_code}: {course_info}")

    return courses_dict

# Fetch all courses and store them in a dictionary
all_courses_dict = fetch_courses()

# Print the dictionary
for course_code, course_info in all_courses_dict.items():
    print(f"{course_code}: {course_info}")

# Define the path to the JSON file
json_file_path = "courses_data_winter_2025.json"

# Write the dictionary to a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(all_courses_dict, json_file, indent=4)

print(f"Data successfully written to {json_file_path}")