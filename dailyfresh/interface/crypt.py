import base64 as b64
 
def xor_encrypt(tips,key):
    '''
    用于加密的程序片段
    tips ：将加密内容
    key  ：密钥
    '''
    ltips=len(tips)
    lkey=len(key)
    secret=[]
    num=0
    for each in tips:
        if num<=lkey:
            num=num%lkey
            secret.append( chr( ord(each)^ord(key[num]) ) )
            num = num + 1
    return b64.b64encode( "".join( secret ).encode() ).decode()
 
def xor_decrypt(secret,key):
    '''
    用于解密的程序片段
    secret ：加密内容
    key    ：密钥
    '''
    tips = b64.b64decode( secret.encode() ).decode()
    ltips=len(tips)
    lkey=len(key)
    secret=[]
    num=0
    for each in tips:
       if num<=lkey:
            num=num%lkey
            secret.append( chr( ord(each)^ord(key[num]) ) )
            num = num + 1
    return "".join( secret )
 
# tips= '{"datetime": "2021-03-05-21", "name": "jsq"}'
# key= "bga5t#n-a9=mx^glxprkc#16c#z*n_t%o8jiwh(y*i+h7c!xo$"
# secret = 'GUUFVABGGkQMXB9XWHxVXEpBX1tQDgEDThFLCEJ/VksOVQ9LTUgKQBpZG1EVHg=='#xor_encrypt(tips,key)
# print( "cipher_text:", secret )

# plaintxt = xor_decrypt( secret, key )
# print( "plain_text:",plaintxt )
# # #修改自 https://www.zhangshengrong.com/p/ArXGrnqrNj/