class Input_Helper:

	def get_valid_name():
		name = ''
		while True:
			name = input('\nPlease enter the name of the new account: ')
			if '<~>' in name:
				print('\nSorry, but it is not possible to use "<~>" inside the name.\nPlease try another name.\n')
				# This is because '<~>' is used by the program as a separator.
				continue
			if len(name) >= 3:
				return name
			else:
				print('\nToo short. The account name must have a minimum of 3 characters.\n')

	def create_password():
		pw = 1
		pw_repeat = 0
		while True:
			pw = input('\nChoose the password for your new account: ')
			if '<~>' in pw:
				print('\nSorry, but it is not possible to use "<~>" inside the password.\nPlease try another password.\n')
				# This is because '<~>' is used by the program as a separator.
				continue
			if not (len(pw) >= 5):
				print('\nThe password must have 5 characters minimum.\nPlease try again.')
				continue
			pw_repeat = input('Please enter the password again: ')
			if not pw == pw_repeat:
				print('\nError: The two entered passwords are different.\nPlease try again.')
			else:
				print('\nPassword was set successfully.\n')
				break
		return str(pw)
	
	def get_confirmation(name, action):
		while True:
			confirm = input(f'\nAre you sure you want to {action} this account: "{name}" ?\n\n\t"Y" - Yes\n\t"N" - No\n\t\t')
			if confirm in ('y', 'Y', 'n', 'N'):
				if confirm in ('y', 'Y'):
					return True
				else:
					return False
			else:
				print('\nInvalid input!')
	
	def get_valid_account_action(account_name):
		while True:
			action = input(f'\nWhat you want to do with your account "{account_name}"?\n\n\t"S" - See account balance\n\t"W" - Withdraw\n\t"D" - Deposit\n\t"R" - Remove account\n\t"N" - Nothing. Go back to main page.\n\t\t')
			if action in ('s', 'S', 'w', 'W', 'd', 'D', 'r', 'R', 'n', 'N'):
				return action.upper()
			else:
				print('\nInvalid input!')
	
	def get_valid_transaction_amount(action):
		transtype = 'withdraw' if action == 'W' else 'deposit'
		while True:
			amount = input(f'\nHow much do you want to {transtype}?\n\n\tEnter amount: ')
			if ',' in amount:
				amount = amount.replace(',', '.')
			try:
				amount = float(amount)
			except ValueError:
				print('\nInvalid input. Please enter a number!')
				continue
			if '.' in str(amount):
				if len(str(amount).split('.')[1]) > 2:
					print('\nToo many decimals (max=2) !')
					continue
			if amount < 0:
				print(f'\nInvalid input. The amount {transtype}ed must be positive.')
			else:
				return float(amount)
			
	def get_try_again(try_again):
		while True:
			if try_again in ('y', 'Y'):
				return True
			elif try_again in ('n', 'N'):
				return False
			else:
				try_again = input('\nInvalid input! Please enter "y" or "n":  ')




class Account:

	def __init__(self, name, password, balance):
		self.name = name
		self.password = password
		self.balance = balance

	def show_balance(self):
		print(f'\nBalance of account "{self.name}" is:   $ {self.balance}\n')

	def check_password(self):
		while True:
			userinput = input(f'\nPlease enter the password for the account {self.name}: ')
			if userinput == self.password:
				return True
			else:
				print('Password incorrect!')
				choice = input('\nDo you want to try again? y/n ')
				confirmation = Input_Helper.get_try_again(choice)
				if not confirmation:
					return False
	
	def execute_transaction(self, action, amount):
		transfer_happened = False
		transtype = 'withdraw' if action == 'W' else 'deposit'
		if transtype == 'withdraw':
			if self.balance < amount:
				print("\nSorry, but this is not possible!\nYou don't have enough money!\n")
				return self.something_else_question(transfer_happened)
		relword = 'from' if action == 'W' else 'to'
		confirmation = input(f'\nYou are about to {transtype}   $ {amount}   {relword} your account "{self.name}".\n\n\tAre you sure you want to continue? y/n ')
		while confirmation not in ('y', 'Y', 'n', 'N'):
			confirmation = input('\nInvalid input. Please enter "y" or "n" !\n\t\t')
		if confirmation in ('y', 'Y'):
			if transtype == 'withdraw':
				self.balance -= amount
			else:
				self.balance += amount
			self.balance = round(self.balance, 2)
			print(f'\nYou successfully {transtype}ed ${amount}!\n')
			transfer_happened = True
		else:
			print('\n...cancelling transaction...\n')
		return self.something_else_question(transfer_happened)
	
	def something_else_question(self, transfer_happened):
		choice = input('Do you want to do something else with your account?\n\n\t"Y" - Yes!\n\t"N" - No. Please go back to main page.\n\t\t')
		confirmation = Input_Helper.get_try_again(choice)
		if confirmation:
			return (False, transfer_happened)
		else:
			return (True, transfer_happened)



class Bank:

	def __init__(self, change_state):
		self.change_state = change_state
		self.accounts = self.load_accounts()
		self.active_account = None
		self.transaction_amount = 0

	def load_accounts(self):
		account_data_list = []
		try:
			with open('accounts.txt', 'r') as acc_data:
				account_data_list = acc_data.readlines()
		except FileNotFoundError:
			with open('accounts.txt', 'w'):
				pass
		accounts = {}
		if account_data_list:
			line = 0
			try:
				for a in account_data_list:
					line += 1
					a.strip()
					values = tuple(a.split('<~>'))
					accounts[values[0]] = Account(values[0], values[1], float(values[2]))
			except:
				print(f'Failed to load account at line {line} in file "accounts.txt"')
		return accounts

	def create_account(self):
		name = Input_Helper.get_valid_name()
		while name in self.accounts:
			print('\nSorry, but this name is already used!\nPlease choose another one.\n')
			name = Input_Helper.get_valid_name()
		password = Input_Helper.create_password()
		confirmation = Input_Helper.get_confirmation(name, 'create')
		if confirmation:
			new_account = Account(name, password, 0)
			self.accounts[name] = new_account
			self.active_account = new_account
			with open('accounts.txt', 'a') as acc_file:
				acc_file.write(f'{name}<~>{password}<~>0\n')
			print(f'\nYou successfully created the account: "{name}"!\n')
			self.change_state('account action')
		else:
			print("\nAccount creation cancelled!\n")
			self.change_state('start')
	
	def delete_account(self):
		name = self.active_account.name
		confirmation = Input_Helper.get_confirmation(name, 'delete')
		if confirmation:
			if not self.active_account.balance:
				del self.accounts[name]
				with open('accounts.txt', 'r') as acc_file:
					file_content_list = acc_file.readlines()
				index = 0
				for line in file_content_list:
					line_name = line.split('<~>')[0]
					if line_name == name:
						file_content_list.pop(index)
						break
					index += 1
				new_content = ''.join(file_content_list)
				with open('accounts.txt', 'w') as acc_file:
					acc_file.write(new_content)
				self.active_account = None
				print(f'\nThe following account was deleted: "{name}"\nGoing back to main page.\n')
				self.change_state('start')
			else:
				print(f'Error: Deletion of account "{name}" is not possible!\nReason: The account is NOT empty! Withdraw all the money first!\nCurrent balance:   $ {self.active_account.balance}\n')
				self.change_state('account action')
		else:
			print('\nDeletion cancelled!\n')
			self.change_state('account action')

	def look_up_names(self):
		while True:
			userinput = input('\nPlease enter the name of the account you want to select: ')
			for a in self.accounts:
				if a == userinput:
					return userinput
			try_again = input(f'\nThe account name "{userinput}" '+"doesn't exist.\nTipp: Please also take care of upper case and lower case characters.\n\n\tDo you want to try again? y/n ")
			confirmation = Input_Helper.get_try_again(try_again)
			if not confirmation:
				return None

	def handle_account_selection(self):
		selection = self.look_up_names()
		if selection:
			access_granted = self.accounts[selection].check_password()
			if access_granted:
				self.active_account = self.accounts[selection]
				self.change_state('account action')
			else:
				self.change_state('start')
		else:
			self.change_state('start')
	
	def dump_transaction(self):
		with open('accounts.txt', 'r') as acc_file:
			file_content_list = acc_file.readlines()
		index = 0
		for line in file_content_list:
			line_list = line.split('<~>')
			if line_list[0] == self.active_account.name:
				line_list[2] = str(self.active_account.balance)
				file_content_list[index] = '<~>'.join(line_list)+'\n'
				break
			index += 1
		new_content = ''.join(file_content_list)
		with open('accounts.txt', 'w') as acc_file:
			acc_file.write(new_content)

	def handle_account_action(self):
		action = Input_Helper.get_valid_account_action(self.active_account.name)
		if action in ('W', 'D'):
			amount = Input_Helper.get_valid_transaction_amount(action)
			back2main, transfer_happened = self.active_account.execute_transaction(action, amount)
			if transfer_happened:
				self.dump_transaction()
			if back2main:
				self.change_state('start')
				self.active_account = None
			else:
				self.change_state('account action')
		elif action == 'S':
			self.active_account.show_balance()
			self.change_state('account action')
		elif action == 'R':
			self.delete_account()
		else:
			self.change_state('start')
	
   

class App:

	def __init__(self):
		self.current_state = 'start'
		self.bank = Bank(self.change_state)
		print('\n\nHello and welcome to the little bank app!\n')
		self.handle_next_step()

	def change_state(self, state):
		self.current_state = state
		self.handle_next_step()

	def handle_start(self):
		userinput = ""
		while not userinput in ('c', 'C', 's', 'S', 'q', 'Q'):
			userinput = input('\nWhat would you like to do?\n\n\t"C" - Create a new account.\n\t"S" - Select an existing account.\n\t"Q" - Quit application.\n\t\t')
			if userinput in ('c', 'C'):
				self.change_state('account creation')
			elif userinput in ('s', 'S'):
				self.change_state('account selection')
			elif userinput in ('q', 'Q'):
				print('\n\nThank you for using the little bank app.\n\nGood Bye!\n\n')
			else:
				print('\nInvalid input!\n')

	def handle_next_step(self):
		match self.current_state:
			case 'start':
				self.handle_start()
			case 'account creation':
				self.bank.create_account()
			case 'account selection':
				self.bank.handle_account_selection()
			case 'account action':
				self.bank.handle_account_action()

App()
