from PIL import Image
import numpy as np
import hashlib, json, os
import probability as prob

# Keep track of shibas metadata
allmetadata = []
# Keep track of shibas created
shibaCreated = 0
# Keep track of filehashes
fileHashes = []

# Shibas
shibas = ['shiba.png', 'alien.png', 'ape.png', 'clown.png', 'zombie.png']
shibaTypes = ['classic', 'alien', 'ape', 'clown', 'zombie']
backgrounds = ['blue.png', 'yellow.png', 'green.png']

def generateShiba(shibaType):
    # Metadata dictionary to keep track of attributes
    metadata = {}
    if shibaType == 'classic':
        attrDict = prob.Attr
        shibaStack = Image.open(f"basic/{shibas[0]}")
        metadata['Shiba Type'] = 'classic'
    elif shibaType == 'alien':
        attrDict = prob.Attr
        shibaStack = Image.open(f"basic/{shibas[1]}")
        metadata['Shiba Type'] = 'alien'
    elif shibaType == 'ape':
        attrDict = prob.Attr
        shibaStack = Image.open(f"basic/{shibas[2]}")
        metadata['Shiba Type'] = 'ape'
    elif shibaType == 'clown':
        attrDict = prob.Attr
        shibaStack = Image.open(f"basic/{shibas[3]}")
        metadata['Shiba Type'] = 'clown'
    elif shibaType == 'zombie':
        attrDict = prob.Attr
        shibaStack = Image.open(f"basic/{shibas[4]}")
        metadata['Shiba Type'] = 'Zombie'

    attributeCount = 0
    #basedir = f"attributes/{shibaType}/"
    hasEyesAttr = np.random.choice([True, False], p=[0.7, 0.3])
    if hasEyesAttr:
        eyesAttrs = [f"eyes/{item[0]}" for item in attrDict['eyes'].items()]
        eyesChoice = Image.open(np.random.choice(eyesAttrs, p=list(attrDict['eyes'].values())))
        shibaStack.paste(eyesChoice, (0, 0), eyesChoice)
        attributeCount += 1
        metadata['Eyes'] = str(eyesChoice.filename.split("/")[-1])
    hasHeadAttr = np.random.choice([True, False], p=[0.7, 0.3])
    if hasHeadAttr:
        headAttrs = [f"head/{item[0]}" for item in attrDict['head'].items()]
        headChoice = Image.open(np.random.choice(headAttrs, p=list(attrDict['head'].values())))
        shibaStack.paste(headChoice, (0, 0), headChoice)
        attributeCount += 1
        metadata['Head Attribute'] = str(headChoice.filename.split("/")[-1])

    metadata['Total Attributes'] = attributeCount
    print(f"Creating {shibaType} with {attributeCount} attributes")
    allmetadata.append(metadata)
    return shibaStack


# While loop for total number of shibas to be generated
while shibaCreated < 100:

    # Select shibas and start stacking randomly chosen layers using the appropriate function
    output = generateShiba(np.random.choice(shibaTypes, p=[0.5, 0.15, 0.25, 0.02, 0.08]))

    fileHash = hashlib.md5(output.tobytes())
    hashDigest = fileHash.hexdigest()
    if hashDigest not in fileHashes:
        fileHashes.append(hashDigest)
        shibaBg = Image.open(f"backgrounds/{np.random.choice(backgrounds, p=[0.7, 0.2, 0.1])}")
        shibaBg.paste(output, (0, 0), output)
        shibaBg.save(f"generated/CryptoShiba_{shibaCreated}.png")
        print(f"Wrote file CryptoShiba_{shibaCreated}.png ({hashDigest})")
        shibaCreated += 1

with open(f"generated/metadata.json", "w") as outFile:
    json.dump(allmetadata, outFile)
