import sys

OPTIONS = {
  'h' : (lambda x: print('h')),
  'c' : (lambda x: print('c'))
}
help = lambda x: print('Invalid option!')

def main():
  print('Welcome to MegaSenha!')
  options()
  for line in sys.stdin:
    words = line.strip().split(' ')
    c = words.pop(0)
    (OPTIONS.get(c) or help)(words)
    options()
  
def options():
  print('What do you want to do?')
  print('h - host')
  print('c - connect')

main()
