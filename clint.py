import base.amtop as amtop
import threading





thred = threading.Thread(target=amtop.server())
thred.start()


print("""+ for addition, - for subtraction, * for multiplication, / for division""")
input1 = input("enter a opration to perform: ")
print("enter the numbers to perform the operation on")
input2 = input("enter the first number: ")
input3 = input("enter the second number: ")


Problem = {
    "data": {
        "num1": input2,
        "num2": input3,
        "do": input1
    }
}

paylode = amtop.messagemaker("Compute", Problem)
print(paylode)