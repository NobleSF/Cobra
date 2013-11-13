function encrypt(article_id, ip_address):
    chars = list('tmBcAJLT9fXlFwzVYndhMaqQxkGpNr8vUD6uKjZs43WHCg2yE-e7RbP')
    base = len(chars)
    hash_string = []

    ip_address.replace('.','')
    
    for power in reversed(range(2)):
        char = chars[article_id % (base**power)]
        string.append(char)
        article_id = article_id / (base**power)

    for power in reversed(range(7)):
        char = chars[ip_address % (base**power)]
        string.append(char)
        article_id = ip_address / (base**power)

    #turn the list into a string
    return ''.join(hash_string)

function decrypt(hash_string):
    chars = list('tmBcAJLT9fXlFwzVYndhMaqQxkGpNr8vUD6uKjZs43WHCg2yE-e7RbP')
    base = len(chars)

    article_hash = hash_string[0:2]
    ip_address_hash = hash_string[2:9]
    
    article_id = 0
    ip_address = 0

    power = 0
    for char in article_hash:
        article_id += chars.index(char) * (base**power)
        power += 1

    power = 0
    for char in ip_address_hash:
        ip_address += chars.index(char) * (base**power)
        power += 1

    return article_id, ip_address

