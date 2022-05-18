import sys

# Creating text files to store user, domain, type, and access data.
usersFile = open("users.txt", "a")
domainsFile = open("domains.txt", "a")
typesFile = open("types.txt", "a")
accessFile = open("accesses.txt", "a")

# Command name validator function
def validateCommandName(command):

    validCommands = ['AddUser', 'Authenticate', 'SetDomain', 'DomainInfo', 
    'SetType', 'TypeInfo', 'AddAccess', 'CanAccess']

    isValid = False

    if command[0] in validCommands:
        isValid = True

    return isValid

# Command arugments validator function
def validateCommandArugments(command):

    # AddUser command
    if command[0] == 'AddUser':
        missingPassword = False
		
        if len(command) < 3:
            print("Error: missing operands")
            return

        elif len(command) == 3:
            missingPassword = False
            if command[1] == '' or command[1].isspace():
            	print("Error: username missing")
            	return

        else:
            print("Error: too many arguments for AddUser")
            return

        addUser(missingPassword,command)
        return

    # Authenticate command
    elif command[0] == 'Authenticate':

        if len(command) < 3:
            print("Error: missing operands")
            return

        elif len(command) > 3:
            print("Error: too many arguments for Authenticate")
            return

        authenticateUser(command)
        return

    # SetDomain command
    elif command[0] == 'SetDomain':

        if len(command) < 3:
            print("Error: missing operands")
            return
            
        elif len(command) == 3:
            if command[1] == '' or command[1].isspace():
                print("Error: no such user")
                return

            if command[2] == '' or command[2].isspace():
                print("Error: missing domain")
                return

        elif len(command) > 3:
            print("Error: too many arguments for SetDomain")
            return

        setDomain(command)
        return

    # DomainInfo command
    elif command[0] == 'DomainInfo':

        if len(command) < 2:
            print("Error: missing operands")
            return

        elif len(command) == 2:
            if command[1] == '' or command[1].isspace():
                print("Error: missing domain")
                return

        elif len(command) > 2:
            print("Error: too many arguments for DomainInfo")
            return        

        domainInfo(command)
        return

    # SetType command
    elif command[0] == 'SetType':

        if len(command) < 3:
            print("Error: missing operands")
            return

        elif len (command) == 3:
            if command[1] == '' or command[1].isspace():
                print("Error: missing object")
                return
            
            elif command[2] == '' or command[2].isspace():
                print("Error: missing type")
                return

        elif len(command) > 3:
            print("Error: too many arguments for SetType")
            return

        setType(command)
        return

    # TypeInfo command
    elif command[0] == 'TypeInfo':

        if len(command) == 1:
            print("Error: missing operands")
            return

        elif len(command) == 2:
            if command[1] == '' or command[1].isspace():
                print("Error: missing type")
                return

        elif len(command) > 2:
            print("Error: too many arguments for TypeInfo")
            return

        typeInfo(command)
        return    

    # AddAccess command
    elif command[0] == 'AddAccess':

        if len(command) < 4:
            print("Error: missing operands")
            return

        elif len(command) == 4:
            if command[1] == '' or command[1] == 'null' or command[1].isspace():
                print("Error: missing operation")
                return
            elif command[2] == '' or command[2] == 'null' or command[2].isspace():
                print("Error: missing domain")
                return
            elif command[3] == '' or command[3] == 'null' or command[3].isspace():
                print("Error: missing type")
                return

        elif len(command) > 4:
            print("Error: too many arguments for AddAccess")
            return

        addAccess(command)
        return

    # CanAccess command
    elif command[0] == 'CanAccess':

        if len(command) > 4:
            print("Error: too many arguments for CanAccess")
            return

        canAccess(command)
        return

    return

# AddUser command
def addUser(missingPassword, command):

    password = ""

    if missingPassword == False:
        password = command[2]
    
    username = command[1]
    
    # Open users file to check if username exists
    with open("users.txt", "r") as f:
        
        for line in f:
            userData = line.split(' ',1)
            if userData[0] == username:
                print("Error: user exists")
                f.close()
                return
      
    users = open("users.txt", "a")
    userData = username + " " + password + "\n"
    users.write(userData)
    users.close()
    print("Success")

    return

# Authenticate command
def authenticateUser(command):

    password = ""
    username = command[1]

    with open("users.txt", "r") as f:
        
        for line in f:
            userData = line.split(' ',1)
            if userData[0] == username:
                if userData[1].strip("\n") == '' and len(command) == 2:
                    print("Success")
                    return
                elif len(command) == 3 and userData[1].strip("\n") == command[2]:
                    print("Success")
                    return
                else:
                    print("Error: bad password")
                    return
        f.close()
                    
    print("Error: no such user")
    return

# SetDomain command
def setDomain(command):

    username = command[1]
    domainName = command[2]
    
    # Open users file to check if user exists
    with open("users.txt", "r") as f:
        
        userExists = False
        
        for line in f:
            userData = line.split(' ',1)
            if userData[0] == username:   
                userExists = True
                break       
                    
        f.close()
        
        if userExists == False:
            print("Error: no such user")
            return
           
    domainExists = False
    
    # Open domains file to check if domain already exists
    with open("domains.txt", "r") as f:
                      
        lineNum = 0

        for number, line in enumerate(f):
            userData = line.split(' ',1)

            if userData[0] == domainName or domainName == line.strip():
                lineNum = number
                domainExists = True
                break
                
        f.close()

    # If domain exists, add user to the domain or leave unchanged if user already in domain
    if domainExists == True:
        domains = open("domains.txt", "r")
        lines = domains.readlines()
       
        domainSplit = lines[lineNum].strip().split(' ',1)
        
        if len(domainSplit) == 1:
            lines[lineNum] = lines[lineNum].strip() + " " + username + "\n"
            domains = open("domains.txt", "w")
            domains.writelines(lines)
            domains.close()
            print("Success")
            return
            
        userSplit = domainSplit[1].split(' ')
       
        if username in userSplit:
            print("Success")
            return
        
        lines[lineNum] = lines[lineNum].strip() + " " + username + "\n"

        domains = open("domains.txt", "w")
        domains.writelines(lines)
        domains.close()
        
    # If domain does not exist, create it and add the user
    else:
        domains = open("domains.txt", "a")
        domains.write(domainName + " " + username + "\n")
        domains.close()
        
    print("Success")    
    return

# DomainInfo command
def domainInfo(command):

    domainName = command[1]

    with open("domains.txt", "r") as f:

        for line in f:
            domain = line.split(' ',1)
            if domain[0] == domainName:   
                usersList = domain[1].strip().split(' ')
                print(*usersList, sep="\n")
                return     
                    
        f.close()

    return
    
# SetType command
def setType(command):

    objectName = command[1]
    typeName = command[2]
           
    typeExists = False
    
    # Open types file to check if type already exists
    with open("types.txt", "r") as f:
                      
        lineNum = 0

        for number, line in enumerate(f):
            userData = line.split(' ',1)
            if userData[0] == typeName or typeName == line.strip():
                lineNum = number
                typeExists = True
                break
                
        f.close()
    
    # If type exists, add object to the type or leave unchanged if object already in type
    if typeExists == True:
        types = open("types.txt", "r")
        lines = types.readlines()
        
        typeSplit = lines[lineNum].strip().split(' ',1)
        
        if len(typeSplit) == 1:
            lines[lineNum] = lines[lineNum].strip() + " " + objectName + "\n"
            types = open("types.txt", "w")
            types.writelines(lines)
            types.close()
            print("Success")
            return
        
        objectSplit = typeSplit[1].split(' ')

        if objectName in objectSplit:
            print("Success")
            return
        
        lines[lineNum] = lines[lineNum].strip() + " " + objectName + "\n"
        
        types = open("types.txt", "w")
        types.writelines(lines)
        types.close()
    # If type does not exist, create it and add the object
    else:
        types = open("types.txt", "a")
        types.write(typeName + " " + objectName + "\n")
        types.close()
        
    print("Success")    
    return

# TypeInfo command
def typeInfo(command):

    typeName = command[1]

    with open("types.txt", "r") as f:

        for line in f:
            typeN = line.split(' ',1)
            if typeN[0] == typeName:   
                usersList = typeN[1].strip().split(' ')
                print(*usersList, sep="\n")
                return     
                    
        f.close()

    return
    

def addAccess(command):

    operation = command[1]    
    domainName = command[2]
    typeName = command[3]
    
    domainTypeExists = False
    
    # Open users file to check if domain,type exists
    with open("accesses.txt", "r") as f:
                      
        lineNum = 0
        
        domainExists = False
        typeExists = False

        for number, line in enumerate(f):
            accessData = line.split(' ')
            if accessData[0] == domainName and accessData[1] == typeName:
                domainTypeExists = True
                lineNum = number
                break
                
            if accessData[0] == domainName:
                domainExists = True
                
            if accessData[1] == typeName:
                typeExists = True
                
        f.close()

    if domainTypeExists == True:
        access = open("accesses.txt", "r")
        lines = access.readlines()
       
        domainTypeSplit = lines[lineNum].strip().split(' ',2)
        operationSplit = domainTypeSplit[2].split(' ')

        if operation in domainTypeSplit[2]:
            print("Success")
            return
        
        lines[lineNum] = lines[lineNum].strip() + " " + operation + "\n"

        access = open("accesses.txt", "w")
        access.writelines(lines)
        access.close()
        
    elif (domainExists == True and typeExists == False) or (typeExists == True and domainExists == False):
        access = open("accesses.txt", "r")
        lines = access.readlines()
        
        lines[lineNum] = domainName + " " + typeName + " " + operation + "\n"

        access = open("accesses.txt", "a")
        access.writelines(lines)
        access.close()
       
    else:
        access = open("accesses.txt", "a")
        accessData = domainName + " " + typeName + " " + operation + "\n"
        access.write(accessData)
        access.close()
        
    with open("domains.txt", "r") as f:

        domainExists = False
        for number, line in enumerate(f):
            userData = line.split(' ',1)
            if userData[0] == domainName or domainName == line.strip():
                domainExists = True
                break
                
        f.close()
        
    if domainExists == False:
        domains = open("domains.txt", "a")
        domains.write(domainName + "\n")
        domains.close()    
        
    with open("types.txt", "r") as f:
    
        typeExists = False
        for number, line in enumerate(f):
            userData = line.split(' ',1)
            if userData[0] == typeName or typeName == line.strip():
                typeExists = True
                break
                    
        f.close()
        
    if typeExists == False:
        types = open("types.txt", "a")
        types.write(typeName + "\n")
        types.close()
        
    print("Success")
    return


def canAccess(command):

    operation = command[1]
    user = command[2]
    objectName = command[3]

    with open("domains.txt", "r") as f:  
        for line in f:
            domainUsers = line.strip().split(' ')
            if user in domainUsers[1:]:   
                currDomain = domainUsers[0]
                
                with open("types.txt", "r") as g:
                    for line in g:
                        typeObjects = line.strip().split(' ')  
                        if objectName in typeObjects[1:]:   
                            currType = typeObjects[0]
                            
                            with open("accesses.txt", "r") as h:
                                for line in h:
                                    domainTypeSplit = line.strip().split(' ')  
                                    thisDomain = domainTypeSplit[0]
                                    thisType = domainTypeSplit[1]
                                    
                                    if currDomain == thisDomain and currType == thisType:
                                        if operation in domainTypeSplit[2:]:
                                            print("Success")
                                            return
                            h.close()                
                g.close()             
                            
        f.close()
    
    print("Error: access denied")
    return


def main():
    # Taking command line arguments
    command = sys.argv[1:]

    isValid = validateCommandName(command)        
        
    if isValid == True:
    	# Validating further supplied arguments
    	validateCommandArugments(command)

    else:
    	# Invalid command name
    	print("Error: invalid command " + command[0])


if __name__ == "__main__":
    main()
