import openai
import time
import pickle
from forex_python.converter import CurrencyRates


c = CurrencyRates()
price_ind = c.get_rate('USD','INR')

#Session Cost
cost = 0


f = open('Cost.bin' , 'rb')
a = pickle.load(f)

#Total Cost over time
tcost = a['cost']

f.close()

openai.api_key = 'YOUR API KEY'
mt = input("Enter the maximum token length (max 8192) : ")
if mt=='' :
    mt='4000'
t = input("Enter the temperature (0-2) : ")
if t=='' :
    t='0.6'


print ("Enter System messages if any (or press enter) : ",end='')
system = input()

print ("Enter your input message : ",end='')
user = input()



inp = [{'role' : 'system' ,'content' : system },{'role' : 'user' ,'content' : user}]
while (True) :
    result  = openai.ChatCompletion.create(model='gpt-4' , messages=inp , max_tokens=int(mt), temperature=float(t))
    print ("Stop reason : " ,result['choices'][0]['finish_reason'] )
    print ("Gpt 4 : ",result['choices'][0]['message']['content'])
    print ('\nTotal Tokens used for this prompt : ' , result['usage']['prompt_tokens'])
    print ('Total tokens used for the result : ' , result['usage']['completion_tokens'])
    print ('Total tokens : ' ,result['usage']['total_tokens'])
    print ('Total price of your prompt + output = Rs.',((result['usage']['prompt_tokens']*(0.03/1000))+(result['usage']['completion_tokens']*(0.06/1000)))*price_ind)
    cost += ((result['usage']['prompt_tokens']*(0.03/1000))+(result['usage']['completion_tokens']*(0.06/1000)))*price_ind
    print ('\n')
    print ('1) Continue with same context')
    print ('2) Start a new conversation')
    print ('3) Exit program')
    w = int(input("Enter your choice : "))
    if (w==1) :
        inp.append({'role' : 'assistant' , 'content' : result['choices'][0]['message']['content']})
        print ("Enter your input message : ",end='')
        user = input()
        inp.append({'role' : 'user' , 'content' : user})
        continue
    elif (w==2) :
        mt = input("Enter the maximum token length (max 8192) : ")
        t = input("Enter the temperature (0-2) : ")


        print ("Enter System messages if any (or press enter) : ",end='')
        system = input()

        print ("Enter your input message : ",end='')
        user = input()


        inp = [{'role' : 'system' ,'content' : system },{'role' : 'user' ,'content' : user}]
    elif (w==3) : 
        break
    else : 
        print ('Invalid option exiting program')
        break
print ('\n\n')
print ('Session cost : ',cost)
print ('Accumalated cost : ',cost+tcost)
time.sleep(3)
f = open('Cost.bin' , 'wb')
pickle.dump({'cost' : cost+tcost},f)
f.close()
