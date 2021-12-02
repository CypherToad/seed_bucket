# Seed Bucket

Simple sharding of Bitcoin mnemonic words for more compact
representation.

## The idea

By breaking our **2048** seed words into **8** buckets leaves us with **256**
words for bucket.

```
>>> 2048 / 8
256
```

We can use a **single character** to represent the **bucket position** where the **word** is found;
additionally, using separate character sets to represent the **bucket position** and **word** will allow for known **break points** in a multi word seed phrase.

## Bucket position

Using the **last 8 letters of ascii** as single character bucket positions:

```
>>> list(ascii_lowercase[-8:])
['s', 't', 'u', 'v', 'w', 'x', 'y', 'z']
```

## Word

We will need a way to represent 0 - 255, using **2 hex characters** we can do just that:

```
>>> hex(0)
'0x0'
>>> hex(25)
'0x19'
>>> hex(255)
'0xff'
```

We can also trim our `0x` hex identifier to save space

```
>>> hex(0).replace('0x', '')
'0'
>>> hex(25).replace('0x', '')
'19'
>>> hex(255).replace('0x', '')
'ff'
```
