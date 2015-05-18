import hashlib, math, string, random



class HyperLogLog(object):

  
  def __init__(self, registers=512):
    self.registers = registers
    self.registry = [0 for i in range(registers)]
    self.key_len = int(math.log(registers, 2))
    self.items = set()
    
  def gen_index_and_pattern(self, val):
    hexhash = hashlib.sha1(val).hexdigest()
    bithash = bin(int(hexhash,16))[2:]
    idx = int(bithash[-self.key_len:], 2)
    pat = bithash[-(64-self.key_len):-self.key_len]
    return (idx,pat)

  def count_leading_zeros(self, bits): 
    count = 1
    for i in range(-1, -(len(bits)+1), -1): 
      if int(bits[i]) == 0:
        count = count+1
      else:
        break
    return count
    
  def add(self, value):
    idx, pattern = self.gen_index_and_pattern(value)
    leading_zero_count = self.count_leading_zeros(pattern)
    self.registry[idx] = max(self.registry[idx], leading_zero_count)
    self.items.add(value)
    
  def getEstimatedCardinality(self):
    longest_run = reduce(lambda x,y: max(x,y), self.registry)
    simple_estimate = 2 ** longest_run
    hll_estimate =  0.719 * float(self.registers ** 2) / sum(math.pow(2.0, -x) for x in self.registry)
    actual_cardinality = len(self.items)
    return simple_estimate, hll_estimate, actual_cardinality
      
  @classmethod
  def test(cls, count=100000, registers=512):
    hll = HyperLogLog(registers)
    for i in range(count):
      #r = int(random.random() * 100000000)
      r = "".join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for n in range(30)])
      hll.add(str(r))
    print hll.getEstimatedCardinality()
 
  if __name__ == "__main__":
      from hll import HyperLogLog
      import sys
      items = 100000
      if len(sys.argv) == 2:
          items = int(sys.argv[1])
      HyperLogLog.test(count=items)
