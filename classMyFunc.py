class MyClass:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def my_method(self):
        print("Var1:", self.var1)
        print("Var2:", self.var2)




# Create an object of MyClass
obj = MyClass("Hello", 42)

# Access the instance variables
print(obj.var1)  # Output: Hello
print(obj.var2)  # Output: 42

# Call the method on the object
obj.my_method()
# Output:
# Var1: Hello
# Var2: 42
