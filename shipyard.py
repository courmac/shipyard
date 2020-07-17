import random


class Shipyard:
    # create container id's to pass into container
    class Container:
        # creat package id's to pass into package class

        # def can_add_package -- check weight
        # def inert_package
        class Package:

            def __init__(self, owner, dest, idnum, weight, next):
                self._owner = owner
                self._dest = dest
                self._weight = weight
                self._id = idnum
                self._next = next
                return

        # ------------------------------------------------------
        # CONTAINER

        def __init__(self, dest, conid,  next):
            self._first = None
            self._size = 0
            self._dest = dest
            self._weight = 0
            self._containerid = conid
            self._next = next

        def __len__(self):
            ''''Returns number of packages in container'''
            return self._size

        def isConEmpty(self):
            '''true if container is empty'''
            return len(self) == 0

        def create_pacid(self):
            '''Creates a random package id starting with p followed by 4 digits'''
            pacid = 'p'
            pacid += str(random.randint(1000, 10000))
            return pacid

        def add_package(self, owner, dest, weight):
            ''' check for other containers going to same place'''
            idnum = self.create_pacid()
            if (self.isConEmpty() or weight < self._first._weight):
                # if container is empty or
                # if the weight is the lightest
                self._size += 1
                self._first = self.Package(
                    owner, dest, idnum, weight, self._first)
                return

            tempr = self._first
            while (tempr._next != None and weight >= tempr._next._weight):
                tempr = tempr._next
            # adds package where it belongs in relation to weights
            self._size += 1
            tempr._next = self.Package(owner, dest, idnum, weight, tempr._next)

            return

    # ---------------------------------------------------------------
    # SHIPYARD

    def __init__(self):
        self._first = None
        self._size = 0

    def __len__(self):
        '''Returns number of containers'''
        return self._size

    def isEmpty(self):
        '''Returns true is no containers in shipyard'''
        return len(self) == 0

    def __repr__(self):
        '''NEED TO FIGURE OUT WHAT THIS IS SUPPOSED TO DO @ PRINT(S)!!!!!!!!!!!!!!!!!!!!!!!!!!'''
        currentcontainers = ''
        tempref = self._first
        while tempref != None:
            # printing out container id's
            cuurentcontainers += tempref._containerid
            tempref = tempref._next
        # temp ref create string and add to
        # must print out sontainer in shipyard
        return currentcontainers

    def isPresent(self, dest, weight):
        '''Traverses containers till destination is found
        Returns container object if container exists and package can fit
        else returns False'''
        tmpRef = self._first
        while(tmpRef != None):
            if tmpRef._dest == dest:
                if int(tmpRef._weight) + int(weight) <= 2000:
                    # make sure it does not put container overweight
                    return tmpRef

            tmpRef = tmpRef._next  # cycle through containers
        return None

    def create_conid(self):
        '''creates container id starting with c and ending with 4 random numbers'''
        conid = 'c'
        conid += str(random.randint(1000, 10000))
        return conid

    def add(self, owner, dest, weight):
        ''' adds package to available container if it exists, 
        else creates new container for package'''
        # container = container to same dest that package can be added to
        # (weight checked)
        container = self.isPresent(dest, weight)
        if container != None:
            # container already exists
            container.add_package(owner, dest, weight)  # call add_package
            container._weight += weight
            print()
            print('Package added to container', container._containerid,
                  'to', container._dest.capitalize())
        else:
            # Container to destination does not exist so must create it
            conid = self.create_conid()
            # create container id

            # See if the new element will be inserted as _first; alphabetically
            if self.isEmpty() or dest < self._first._dest:
                self._size += 1
                # create container object in shipyard class
                self._first = self.Container(dest, conid, self._first)
                self._first._weight += weight
                self._first.add_package(
                    owner, dest, weight)  # call add_package

                print()
                print('Package added to new container',
                      self._first._containerid, 'to', self._first._dest.capitalize())
                return
            # transverse containers for where insertion point is alphabetically
            # Will advance until we hit the end of the list
            else:
                tmpRef = self._first
                while(tmpRef._next != None and dest >= tmpRef._next._dest):
                    tmpRef = tmpRef._next  # cycle through containers

                self._size += 1
                tmpRef._next = self.Container(dest, conid, tmpRef._next)
                # insert container after reference

                tmpRef._next.add_package(
                    owner, dest, weight)  # call add_package
                tmpRef._next._weight += weight  # add package weight to container weight
                print()
                print('Package added to new container', tmpRef._next._containerid,
                      'to', tmpRef._next._dest.capitalize())
            return

    def check_weight(self, conid, weight):
        '''Checks weight of container and returns true if package can fit
        else False'''
        tmpRef = self._first
        while tmpRef != None:  # cycle through every container
            if conid == tmpRef._containerid:  # search for container
                if (weight + int(tmpRef._weight)) <= 2000:  # check if it fits
                    return True

            tmpRef = tmpRef._next
        return False

    def ship(self, dest):
        '''
        Takes a user inpuitted destination and searches through every container
        for any that are for said destination and removes them
        Returns the id's of the containers being shipped.
        Reports the number of containers and total weight delivered.
        Reports if no containers are set to ship to destination.
        '''
        if self.isEmpty():
            print()
            print('Shipyard is empty, cannot ship any containers.')
            return
        shipping = 'Containers shipped to ' + dest.capitalize() + ': '
        # string of containers shipped to destination
        shipWeight = 0  # total weight
        conNum = 0  # number of container

        while self._first._dest == dest:  # ships off the first destination alphabetically
            shipping += self._first._containerid + ' '  # add to id list
            shipWeight += self._first._weight  # add to total weight
            conNum += 1     # increase nimber of containers to ship
            self._size -= 1  # reduces shipyard size by one
            self._first = self._first._next  # skip self._first -> removes first

        tmpRef = self._first
        while (tmpRef._next != None):  # cycle through each container
            if (tmpRef._next._dest == dest):
                shipping += tmpRef._next._containerid + ' '  # add to id list
                shipWeight += tmpRef._next._weight  # add to total weight
                conNum += 1  # increase number of containers to ship
                self._size -= 1  # reduces shipyard size by one
                tmpRef._next = tmpRef._next._next
            else:   # if cont goes to dest, the removal shifts each container down
                #     one and you dont have to iterate to next container unless
                tmpRef = tmpRef._next  # destination does not match, then iterate

        if tmpRef._next == None:
            # end of containers
            if conNum == 0:  # no containers to dest
                print('No containers to ship to', dest.capitalize())
                return
            elif conNum == 1:   # one container to ship
                print(shipping)
                print('A total of ', shipWeight,
                      'lbs was shipped in the container.')
                return
            else:
                print(shipping)  # multiples contaniers to ship
                print('A total of ', shipWeight,
                      'lbs was shipped in the containers.')
                return
        return

    def search(self, owner, dest, weight):
        '''Takes the owner, destination and weight as parameters and returns 
        the package if found, notifies user if not found'''
        if self.isEmpty():  # empty shipyard
            print()
            print('Shipyard is empty.')
            return None

        # seaarch for package
        tmpc = self._first  # tmp = first container
        while tmpc != None:
            # if owner, destination and weight match, return the package reference
            if (owner == tmpc._first._owner) and (dest == tmpc._first._dest) and (weight == tmpc._first._weight):
                print()
                print('Found package', tmpc._first._id)
                print('Owned by', tmpc._first._owner.capitalize())
                print('It weighs', tmpc._first._weight, 'lbs')
                print('In container ', tmpc._id)
                print('To ship to', tmpc._first._dest.capitalize())
                print('There are', str(2000 - int(tmpc._weight)) +
                      'lbs still available in this container.')
                return tmpc._first

            tmp = tmpc._first
            # if one doesnt match, iterate till end of packages
            while tmpp._next != None and ((owner != tmpp._owner) or (dest != tmpp._dest) or (weight != tmpp._weight)):
                tmpp = tmpp._next

            if (tmpp._next._owner == owner) and (tmpp._next._dest == dest) and (tmpp._next_weight == weight):
                print()
                print('Found package', tmpp._next._id)
                print('Owned by', tmpp._next._owner.capitalize())
                print('It weighs', tmpp._next._weight, 'lbs')
                print('In container ', tmpp._next._id)
                print('To ship to', tmpp._next._dest.capitalize())
                print('There are', str(2000 - int(tmpc._weight)) +
                      'lbs still available in this container.')
                return tmpp._next
            tmpc = tmpc._next
        # if it reaches here, no package was found
        print()
        print('Package', package_id, 'was not found in shipyard.')
        return None

    def search_by_id(self, package_id):
        '''Takes user inputted package id and searchs shipyard for it
        If found, returns the package reference
        Not found, returns None'''
        if self.isEmpty():
            print()
            print('Shipyard is empty.')
            return None
        # search for package
        tempc = self._first  # tempc container to interate through
        while tempc != None:  # iterate through every container
            if package_id == tempc._first._id:  # first in package list
                print()
                print('Found package', package_id)
                print('Owned by', tempc._first._owner.capitalize())
                print('It weighs', tempc._first._weight, 'lbs')
                print('In container ', tempc._id)
                print('To ship to', tempc._first._dest.capitalize())
                print('There are', str(2000 - int(tempc._weight)) +
                      'lbs still available in this container.')
                return tempc._first

            tempp = tempc._first
            while tempp._next != None and package_id != tempp._next._id:
                # exits at last reference or ref before matching id
                tempp = tempp._next  # cycle through packages in container

            if tempp._next._id == package_id:  # package id found in ._next
                print()
                print('Found package', package_id)
                print('Owned by', tempp._next._owner.capitalize())
                print('It weighs', tempp._next._weight, 'lbs')
                print('In container ', tempp._next._id)
                print('To ship to', tempp._next._dest.capitalize())
                print('There are', str(2000 - int(tempc._weight)) +
                      'lbs still available in this container.')
                return tempp._next
            tempc = tempc._next  # cycle through containers
        # if it reaches here, no package was found
        print()
        print('Package', package_id, 'was not found in shipyard.')
        return None

    def remove(self, owner, dest, weight):
        '''Takes an owner, destination, and weight as parameters and searchs
        for package, if it is found, it removes from it's container
        If it is not found, notifies user'''
        if self.isEmpty():
            print()
            print('Cannot remove package from empty shipyard.')
            return
        # search for the package
        tmpc = self._first
        while tmpc != None:  # iterate till end of container list
            if (tmpc._first._owner == owner) and (tmpc._first._dest == dest) and (tmpc._first._weight == weight):
                # if owner, dest and weight match
                print()  # notify user
                print("Package", tmpc._first._id, " to",
                      dest.capitalize(), "was removed")
                tmpc._size -= 1
                tmpc._first = tmpc._first._next  # remove frist package

                # check for empty container
                # if tempc.isConEmpty():
                #    remove tempc
                return tmpc._first

            tmpp = tmpc._first
            while tmpp._next != None:
                # iterate until end
                if (tmpp._next._owner == owner) and (tmpp._next._dest == dest) and (tmpp._next_weight == weight):
                    print()  # notify user it was found and removed
                    print('Package', tmpp._next._id, 'to',
                          tmpp._next._dest.capitalize(), 'was removed.')
                    tmpc._size -= 1
                    tmpc._next = tmpc._next._next

                    # check for empty container
                    # if tempc.isConEmpty():
                    #    remove tempc
                    return tmpp._next
                else:
                    tmpp = tmpp._next

            tmpc = tmpc._next   # cycle through containers
        # if it reaches here, no package was found
        print()  # if function reaches here, no containers that match were found
        print('Package owned by', owner.capitalize(), 'that weighs', weight,
              'lbs, to', dest.capitalize(), 'was not found in shipyard.')
        return

    def remove_by_id(self, package_id):
        '''Takes user inputted package id and searches each container
        Removes said package if found, notifies user if not found'''
        if self.isEmpty():
            print()
            print('Shipyard is empty, cannot remove package')
            return
        # search for package
        tempc = self._first  # tempc container to interate through
        while tempc != None:  # iterate through every container
            if package_id == tempc._first._id:  # first in package list
                print()
                print('Package', package_id, 'was removed.')
                tempc._size -= 1
                tempc._weight -= tempc._first._weight
                tempc._first = tempc._first._next  # skip first -> remove first

                # check for empty container
                # if tempc.isConEmpty():
                #    remove tempc
                return

            tempp = tempc._first  # tempp iterates through all packages
            while tempp._next != None:  # exits at last reference
                if package_id == tempp._next._id:
                    # package id found in ._next
                    tempc._size -= 1
                    tempc._weight -= tempp._next._weight
                    print()
                    print('Package', tempp._next._id,
                          ' was removed from the shipyard')
                    tempp._next = tempp._next._next  # remove package

                    # check for empty container
                    # if tempc.isConEmpty():
                    #    remove tempc
                    return
                tempp = tempp._next  # cycle through packages in container

            tempc = tempc._next  # cycle through containers

        print()
        print('Package', package_id, ' was not found and cannot be removed.')
        return

    # --------------------

    def printAll(self):
        ''' Prints the whole manifest of the shipyard including containers,
        pacakges and their respective information'''
        # option c

        if self.isEmpty():
            print('Cannot print manifest, shipyard is empty')
            return
        print()
        print('Shipyard Manifest')
        tmp = self._first
        while tmp != None:  # tmp goes through every container
            # Container info : id, dest, weight
            print('-----------------------------')
            print('Id: ', tmp._containerid)
            print('Destination: ', tmp._dest.capitalize())
            print('Weight: ', tmp._weight)
            print()

            tmpp = tmp._first
            while tmpp != None:  # tmpp goes through every package in tmp
                # Package info: owner, id, dest, weight
                print('    ---Packages---')
                print('    Owner: ', tmpp._owner.capitalize())
                print('    Id: ', tmpp._id)
                print('    Destination: ', tmpp._dest.capitalize())
                print('    Weight: ', tmpp._weight)
                tmpp = tmpp._next
            tmp = tmp._next
        return

    def printDest(self, dest):
        '''Prints sipyard manifest for one destination including the
        containers, packages and their respecrive information
        Notifies user if no containers to said destination'''
        # option b
        if self.isEmpty():
            print('Cannot print manifest for',
                  dest.capitalize(), ', shipyard is empty')
            return
        print()
        print('Containers for ', dest.capitalize())
        count = 0
        # if no containers for destination exist, count will == 0 at end of function
        temp = self._first
        while temp != None:
            if temp._dest == dest:
                count += 1
                # Container info
                print('-----------------------------')
                print('Id: ', temp._containerid)
                print('Destination: ', temp._dest.capitalize())
                print('Weight: ', temp._weight)
                print()

                temppac = temp._first
                while temppac != None:
                    # Package info
                    print('    ---Packages---')
                    print('    Owner: ', temppac._owner.capitalize())
                    print('    Id: ', temppac._id)
                    print('    Destination: ', temppac._dest.capitalize())
                    print('    Weight: ', temppac._weight)
                    temppac = temppac._next
            temp = temp._next

        if count == 0:
            # must notify user no containers for dest
            print('Cannot print manifest, there are no containers for',
                  dest.capitalize())
            return
        return

    def printContainers(self):
        '''Prints each container in shipyard including id, destination and weight
        Notifies if shipyard is empty'''
        # option d
        if self.isEmpty():
            print('Cannot print manifest, shipyard is empty')
            return

        print()
        print('All containers in shipyard')
        temp = self._first
        while temp != None:  # cycle through all containers
            print('-----------------------------')
            print('Id: ', temp._containerid)
            print('Dest: ', temp._dest.capitalize())
            print('Weight: ', temp._weight)
            print()

            temp = temp._next
        return

    def traversePrint(self):
        tmpRef = self._first
        while tmpRef != None:  # cycles through every container
            print(tmpRef._elem)
            # not just elem but owner, dest and weight
            tmpRef = tmpRef._next
# --------------------------------------------------------------------------


class Empty(Exception):
    pass


def fix_owner(owner):
    '''Removes extra characters from user inputed owner string for organization ease
    Removes everything but letters and converts to lowercase
    Error check for empty string'''
    while owner == '':
        print('Owner cannot be empty')
        owner = input('Who is the owner: ')
    # takes the owner and removes extraneous info
    owner = owner.lower()
    for elem in owner:
        if elem.isalpha() == False:
            owner = owner.replace(elem, '')
    return owner


def fix_dest(dest):
    '''Removes extra characters from user inputed destination string for organization ease
    Removes everything but letters and converts to lowercase
    Error check for empty string'''
    while dest == '':
        print('Destination cannot be empty')
        dest = input('Where is the destination: ')
    # takes the destinations and removes extraneous info
    dest = dest.lower()
    for elem in dest:
        if elem.isalpha() == False:
            dest = dest.replace(elem, '')
    while dest == '':
        print('Destination must have at least one letter.')
        dest = input('Where is the destination: ')
    return dest


def validate_weight(weight):
    '''Validates that the user inputed weight string can be converted into integer
    Ensures package weight will not put container overweight
    Returns False if no container for package to be added
    Returns container reference if worthy container object exists'''
    try:
        int(weight)
        if int(weight) > 2000:
            print('Sorry, cannot ship anything over 2000lbs.')
            return
        return True
    except:
        print('Weight must be an integer number.')
    return


def validate_pacid(package_id):
    '''Validates user inputted package id for proper format'''
    package_id = package_id.lower()
    if (len(package_id) != 5) or (package_id[0] != 'p') or (package_id[1:].isdigit() == False):
        return None  # None = not valid
    return True  # True = valid


def print_menu():
    '''Prints out the menu'''
    print('''
Menu

a) Add package
b) Print manifest for a destination
c) Print shipyard manifest
d) Print containers in shipyard
e) Search for a package
f) Remove package
g) Ship containers to one destination
h) Exit''')
    return


def main():
    '''Main running function for the program'''
    s = Shipyard()
    print_menu()
    option = input('Please make selection: ')
    '''ASK HOW TO MAKE IT GO THROUGH BOTHER WHILE LOOPS'''

    while option != 'h' or option != 'H':
        # if option == h(H) --> exit program
        while option not in 'ABCDEFGHabcdefgh':
            # ensure valid option
            option = input('Please make a selection from a through h: ')

        if option == 'a' or option == 'A':
            # ADD PACKAGE
            # user input package information
            owner = input('Who is the owner: ')
            owner = fix_owner(owner)
            dest = input('Where is the destination: ')
            dest = fix_dest(dest)
            weight = input('What does this package weigh(lbs): ')
            while validate_weight(weight) != True:
                weight = input('What does this package weigh(lbs): ')
            weight = int(weight)
            # validated information used to add package
            s.add(owner, dest, weight)

        elif option == 'b' or option == 'B':
            # PRINT MANIFEST FOR A DESTINATION
            dest = input('What is the destination: ')
            s.printDest(dest)

        elif option == 'c' or option == 'C':
            # PRINT SHIPYARD MANIFEST
            s.printAll()

        elif option == 'd' or option == 'D':
            # PRINT CONTAINERS IN SHIPYARD
            s.printContainers()

        elif option == 'e' or option == 'E':
            # SEARCH FOR A PACKAGE
            package_id = input('Please enter package id you want to remove: ')
            while validate_pacid(package_id) != True:
                print('Incorrect package id format. (pxxxx where x is a digit)')
                package_id = input(
                    'Please enter package id you want to remove: ')
            s.search_by_id(package_id)

        elif option == 'f' or option == 'F':
            # REMOVE PACKAGE
            package_id = input('Please enter package id you want to remove: ')
            while validate_pacid(package_id) != True:
                print('Incorrect package id format. (pxxxx where x is a digit)')
                package_id = input(
                    'Please enter package id you want to remove: ')
            s.remove_by_id(package_id)

        elif option == 'g' or option == 'G':
            # SHIP CONTAINERS TO ONE DESTINATION
            dest = input('Where is the destination: ')
            dest = fix_dest(dest)
            s.ship(dest)

        else:
            break

        print_menu()
        option = input('Please make selection: ')
    return


def tester():
    # Simple test program for Lab 5
    # Modifications have been made to the test function through my testing
    # and bug checking to fix the code
    # Below is template for different functions to run different tests on
    print('''
    a  t.add(owner, dest, weight)
    b  t.printDest(dest) 
    c  t.printAll()
    d  t.printContainers()
    e  t.search_by_id(package_id)
    f  t.remove_by_id(package_id)
    g  t.ship(dest)''')
    t = Shipyard()
    print()
    print('-------------------------------------------')
    print("t.add('adam', 'alabama', 5)")
    t.add('adam', 'alabama', 5)

    print('-------------------------------------------')
    print("t.add('ok', 'aa', 1900)")
    t.add('ok', 'aa', 1900)

    print('-------------------------------------------')
    print("t.add('ko', 'aa', 900)")
    t.add('ko', 'aa', 900)

    print('-------------------------------------------')
    print("t.add('harry', 'edm', 900)")
    t.add('harry', 'edm', 900)

    print('-------------------------------------------')
    print("t.add('tick', 'cal', 800)")
    t.add('tick', 'cal', 800)

    print('-------------------------------------------')
    print("t.add('jo', 'edm', 30)")
    t.add('jo', 'edm', 30)

    print('-------------------------------------------')
    print("t.add('fred', 'edm', 1999)")
    t.add('fred', 'edm', 1999)

    print('-------------------------------------------')
    print("t.add('tim', 'cal', 600)")
    t.add('tim', 'cal', 600)

    print('-------------------------------------------')
    print("t.add('lo', 'vic', 500)")
    t.add('lo', 'vic', 500)

    t.printAll()

    print('-------------------------------------------')
    print("****Shipping first destination alphabetically****")
    t.ship('aa')
    t.printAll()

    print('-------------------------------------------')
    print("***Shipping middle destination alphabetically***")
    t.ship('edm')
    t.printAll()

    print('-------------------------------------------')
    print("***t.remove('tim', 'cal', 600)***")
    t.remove('tim', 'cal', 600)
    t.printAll()

    print('-------------------------------------------')
    print('Remove by id')
    package_id = input('enter id: ')
    t.remove_by_id(package_id)
    t.printAll()

    print('-------------------------------------------')
    print('Rprint destination')
    dest = input('dest: ')
    t.printDest(dest)

    print('-------------------------------------------')
    print('Rprint destination')
    t.printcontainers()


if __name__ == "__main__":
    main()
