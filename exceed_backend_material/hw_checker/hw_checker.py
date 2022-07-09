import requests

file_object = open('output.txt', 'a')
base_url = "http://158.108.182."
first_ip = [ '1', '3', '14', '17', '26', '28', '30', '32', '38', '41' ]
second_ip = [ '2', '5', '6', '7', '8', '9', '10', '12', '13', '15', '16', '18', '23', '39']

for ip in first_ip:
    file_object.write('-------------------------------\n')
    file_object.write(f'{base_url}{ip}\n')
    for port in range (5001, 5006):
        file_object.write(f'{port}\n')
        
        #GET
        file_object.write('GET ')
        try:
            myReq = requests.get(f"{base_url}{ip}:{port}/homework")
            if (myReq.status_code == 200):
                file_object.write(myReq.text)
            else:
                file_object.write('Manual\n')
        except:
            file_object.write("Down\n")

        #POST
        file_object.write('POST ')
        try:
            myReq = requests.post(f"{base_url}{ip}:{port}/homework", json={"first": 4, "operator": "*", "second": 3})
            if (myReq.status_code == 200):
                file_object.write(myReq.text)
            else:
                file_object.write('Manual\n')
        except:
            file_object.write("Down\n")

        file_object.write('\n')

file_object.close()