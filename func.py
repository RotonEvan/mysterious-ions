import numpy as np

# round constant
def roundconst(i):
    # TODO Use constants
    block = [0] * 16

    for idx in range(4):
        lfsr_in = [0, 0, 0, 0, 0, 0, 0, 0]
        lfsr_in[idx*2 + 1] = i
        tmp = lbox(lfsr_in)
        block[4 * idx] = (tmp[0] << 4) | tmp[1]
        # output.append(block)
    output = np.array(block)
    output = output.reshape(4,4)
    return output

# multiplication in GF-16

def MultiplyGF16(a, b, p=0b10011):
    result = 0
    for _ in range(4):
        result ^= (b & 1) * a
        a <<= 1
        a ^= (a >> 4) * p
        b >>= 1
    return result

# bit-slice

def BitSlice(block):
    bs = 8*[0]
    for i in range(4): 
        for x in range(8): 
            bs[7-x] |= ((block[3-i] & (1 << x)) >> x) << i
    return bs

# bit-slice reverse

def BitSlice_Rev(bs):
    block = 4*[0]
    for i in range(4): 
        for x in range(8): 
            block[3-i] |= ((bs[7-x] & (1 << i)) >> i) << x
    return block

# blocks to state for ShiftColumns

def toState(A,s):
    output = []
    out = []
    for i in range(s):
      for j in range(4):
        input = A[i][j]
        output.append([int(x) for x in '{:08b}'.format(input)])
      out.append(output)
      output = []
    out = np.array(out)
    return out

# state to state list

def StatetoList(a):
  st_list = []
  for i in a:
    for j in i:
      st_list.append(int(''.join('01'[k] for k in j), 2))

  return st_list

def ddt(S):
  ddtArr = [[0 for i in range(16)] for j in range(16)] 
  max =0
  for u in range(16):
    for v in range(16):
      i = u^v
      o = S[u]^S[v]
      ddtArr[i][o] = ddtArr[i][o] +1
  arr = np.array(ddtArr)
  print(arr)

def LAT(S): 
    bits =[0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]
    arr = [[-8 for i in range(15)] for j in range(15)] 
    for i in range(1,16):
        for j in range(1,16):
            for m in range(16):
                c = S[m]
                a = (i)&m
                b = (j)&c
                count = 0
                if (bits[a]%2) == (bits[b]%2): 
                    arr[i-1][j-1] +=1
    latable = np.array(arr)
    print(latable)

# S-box

def Sbox(block):
    a = (block[0] & block[1]) ^ block[2]
    c = (block[1] | block[2]) ^ block[3]
    d = (a & block[3]) ^ block[0]
    b = (c & block[0]) ^ block[1]
    block = [a,b,c,d] 
    return block

# S-box reverse

def sbox_rev(block):
    b = (block[2] & block[3]) ^ block[1]
    d = (block[0] | b) ^ block[2]
    a = (d & block[0]) ^ block[3]
    c = (a & b) ^ block[0]
    return [a, b, c, d]

# L-box

def lbox(state):
    poly = [0, 0b1000, 0b0011, 0b1111, 0b0101, 0b1111, 0b0011, 0b1000]
    for _ in range(8):
        x = state[0]
        for i in range(8):
            x ^= MultiplyGF16(state[i], poly[i])
        state.pop(0)
        state.append(x)
    return state

# L-box reverse

def lbox_rev(state):
    poly = [0b1000, 0b0011, 0b1111, 0b0101, 0b1111, 0b0011, 0b1000, 0]
    for _ in range(8):
        x = state[7]
        for i in range(8):
            x ^= MultiplyGF16(state[i], poly[i])
        state.pop(7)
        state = [x] + state[:]
    return state

def ShiftColumns_128(State):
    State  = np.array(toState(State,4))
    ac11 = State[0][:,:2]
    ac12 = State[0][:,2:4]
    ac13 = State[0][:,4:6]
    ac14 = State[0][:,6:8]

    ac21 = State[1][:,:2]
    ac22 = State[1][:,2:4]
    ac23 = State[1][:,4:6]
    ac24 = State[1][:,6:8]

    ac31 = State[2][:,:2]
    ac32 = State[2][:,2:4]
    ac33 = State[2][:,4:6]
    ac34 = State[2][:,6:8]

    ac41 = State[3][:,:2]
    ac42 = State[3][:,2:4]
    ac43 = State[3][:,4:6]
    ac44 = State[3][:,6:8]

    c0 = np.concatenate((ac11,ac42,ac33,ac24),axis = 1)
    c1 = np.concatenate((ac21,ac12,ac43,ac34),axis = 1)
    c2 = np.concatenate((ac31,ac22,ac13,ac44),axis = 1)
    c3 = np.concatenate((ac41,ac32,ac23,ac14),axis = 1)
    # State = [b1,b2,b3,b4]
    output = [c0,c1,c2, c3]
    # state = toState(output)
    output = StatetoList(output)
    output = np.array(output)
    out = output.reshape(4,4)
    # print(out)
    return out

def ShiftColumns_128_inv(State):
    State  = np.array(toState(State,4))
    ac11 = State[0][:,:2]
    ac12 = State[1][:,2:4]
    ac13 = State[2][:,4:6]
    ac14 = State[3][:,6:8]

    ac21 = State[1][:,:2]
    ac22 = State[2][:,2:4]
    ac23 = State[3][:,4:6]
    ac24 = State[0][:,6:8]

    ac31 = State[2][:,:2]
    ac32 = State[3][:,2:4]
    ac33 = State[0][:,4:6]
    ac34 = State[1][:,6:8]

    ac41 = State[3][:,:2]
    ac42 = State[0][:,2:4]
    ac43 = State[1][:,4:6]
    ac44 = State[2][:,6:8]


    c0 = np.concatenate((ac11,ac12,ac13,ac14),axis = 1)
    c1 = np.concatenate((ac21,ac22,ac23,ac24),axis = 1)
    c2 = np.concatenate((ac31,ac32,ac33,ac34),axis = 1)
    c3 = np.concatenate((ac41,ac42,ac43,ac44),axis = 1)
    # State = [b1,b2,b3,b4]
    output = np.array([c0,c1,c2, c3])
    output = StatetoList(output)
    output = np.array(output)
    output = output.reshape(4,4)
    return output

def Mysterion128(key, m, NR):
  # adding key initially 
  state = np.array( [x ^ y for x, y in zip(key, m)] )

  for round in range(1, NR + 1):
    # spliting message in blocks 
    blocks = [state[i*4:(i+1)*4] for i in range(4)]
    # S-box
    blocks = np.array([Sbox(block) for block in state])

    # L-box
    s = [BitSlice(block) for block in blocks]
    l = [lbox(i) for i in s]
    blocks = np.array([BitSlice_Rev(i) for i in l])

    # ShiftColumns 128-bit
    state = ShiftColumns_128(blocks)

    constant = roundconst(round)
    state = np.array( [x ^ k ^ c for x, k, c in zip(state, key, constant)] )
  return state 

def InvMysterion128(state, key, NR):
  for round in range(NR, 0, -1):
    constant = roundconst(round)
    state = np.array( [x ^ k ^ c for x, k, c in zip(state, key, constant)] )

    blocks = ShiftColumns_128_inv(state)

    # L-box inverse
    s = [BitSlice(block) for block in blocks]
    l = [lbox_rev(i) for i in s]
    blocks = np.array([BitSlice_Rev(i) for i in l])

    # S-box inverse
    state = np.array([sbox_rev(block) for block in blocks])

  msg = np.array( [x ^ y for x, y in zip(key, state)] )
  return msg