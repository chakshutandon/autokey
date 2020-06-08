# Cryptanalysis of Ciphertexts using the Autokey Cipher Scheme

Chakshu Tandon | 03 May 2020

## IDENTIFYING THE CIPHER METHOD

### TRANSPOSITION/PERMUTATION

Transposition Ciphers shift the position of plaintext characters based on a system with no character substitutions. A type of transposition cipher is the Columnar Transposition Cipher. In this system, plaintext is written in rows of fixed width to read off the columns of ciphertext. Keyed variants of the columnar transposition cipher order columns of ciphertext according to some key or keyword (Lasry, Niebel, Kopal, & Wacker, 2017). Frequency analysis of these ciphers do not yield useful information to help decode the ciphertext since the frequency of plaintext characters is exactly the same as the ciphertext. We can use this property, however, to identify if some unknown ciphertext is using some transposition scheme. Specifically, if we suspect that the letter frequency of ciphertext characters is preserved according to some alphabet, it may suggest that a transposition cipher was used. Otherwise, if letter frequencies do not align then either the plaintext is unusual, a different alphabet was used, or some other cipher method is more likely. Letter frequency analysis of the three ciphertexts is shown in the table below. We truncate the results for the most common English letters (Norvig, 2012).

Table 1. Letter frequencies for the top five (5) English alphabet characters.

|   | Ciphertext1 | Ciphertext2 | Ciphertext3 | English |
| - | ----------- | ----------- | ----------- | ------- |
| e | 0.071       | 0.044       | 0.05        | 0.125   |
| t | 0.038       | 0.049       | 0.035       | 0.093   |
| a | 0.038       | 0.054       | 0.033       | 0.08    |
| o | 0.046       | 0.024       | 0.045       | 0.076   |
| i | 0.038       | 0.051       | 0.048       | 0.076   |

We see above that the letter frequencies are not preserved for the top five English letters. Assuming the plaintext is itself normal English text, it is quite unlikely that these are transposition ciphers. Since the analysis shows other ciphertext letters with higher frequency, it is possible these are substitution ciphers. We first look at the simplest form of substitution ciphers below before extending our analysis to more complex ciphers. 

### SIMPLE SUBSTITUTION (MONOALPHABETIC)

Simple substitution or monoalphabetic ciphers fix the cipher alphabet for a given key. This means that every instance of a plaintext character will encode to the same ciphertext letter regardless of the character’s position in the plaintext. Monoalphabetic and other substitution ciphers do not preserve the individual letter frequencies. Instead, frequencies are “swapped” or flattened for more complex substitutions. One of the simplest substitution ciphers, the Caesar Shift Cipher, shifts every plaintext character by the same amount in the new alphabet (Wikipedia, 2020). In monoalphabetic ciphers, we do not expect the letter frequencies themselves to differ greatly from plain English text. We repeat the single letter frequency analysis as above, but instead, for the top letter frequencies in each of the ciphertexts. We truncate the results for the top five most common characters in each text.

Table 2. Letter frequencies for the top five (5) characters in the text.

|   | Ciphertext1 |   | Ciphertext2 |   | Ciphertext3 |   | English |
| - | ----------- | - | ----------- | - | ----------- | - | ------- |
| v | 0.076       | w | 0.059       | h | 0.07        | e | 0.125   |
| h | 0.076       | l | 0.056       | l | 0.06        | t | 0.093   |
| e | 0.071       | f | 0.056       | s | 0.055       | a | 0.08    |
| g | 0.056       | r | 0.056       | x | 0.055       | o | 0.076   |
| l | 0.05        | a | 0.054       | z | 0.052       | i | 0.076   |

We can see the effects of a flatter frequency curve, predominantly in ciphertext 2, but quite noticeable in ciphertexts 1 and 3. Looking at the frequency distributions alone, it is much more difficult to assign a quantitative measure to identify similarities and differences between ciphertexts and English plaintext. We will introduce another measure, the Index of Coincidence (IoC), to be able to much better understand the frequency distribution the texts arise from. Intuitively, the Index of Coincidence provides a measure for the likelihood that two draws without replacement will result in the same character in a given text (Wikipedia, 2019). We would like to compute this probability for all the characters, c, in a given alphabet. Using formula 1 below, we can compute the IoC of a given text and compare it to the IoC of a large body of English plaintext,

```math
IoC=\frac{\sum_{i=1}^{c}{f_i\left(f_i-1\right)}}{N\left(N-1\right)/c}
```

where f_i is the frequency of character i and N is the length of the text. Neither transposition nor monoalphabetic ciphers affect the underlying frequency of individual letters largely preserving the IoC. For English text,

```math
IoC_{expected}=\frac{\sum_{i=1}^{c}f_i^2}{1\c}=0.0667
```

The table below shows the computed IoC for the given ciphertexts as well as a string (300 characters long) generated randomly from atmospheric noise.

Table 3. Index of Coincidence (IoC) for various texts compared to large body of English.

| Ciphertext1 | Ciphertext2 | Ciphertext3 | Random | English |
| ----------- | ----------- | ----------- | ------ | ------- |
| 0.0416      | 0.0405      | 0.0405      | 0.0388 | 0.0667  |

While the IoC for the given ciphertexts appears to be close to the theoretical value of English plaintext, upon closer examination next to a random string, we determine the cipher scheme has changed the letter frequencies in a more drastic way. It is unlikely that a monoalphabetic substitution cipher was used. It is much more likely the cipher scheme is either polygraphic or polyalphabetic. This result also indicates that the letter frequencies are themselves quite flat. It will be difficult to extract much information from the distribution of single letters (or possibly even larger blocks of characters). Instead, we will have to use another approach to recover the plaintext.

### POLYGRAPHIC

Polygraphic ciphers are similar to monoalphabetic ciphers except they operate on blocks of letters at a time. While the IoC calculation in the section above does not immediately rule out a polygraphic cipher, there are a few interesting observations that make such a cipher scheme unlikely. First, a polygraphic cipher requires the length of the text to be a multiple of the block size. Observing the length of the three ciphers, there does not seem to be a single block size that satisfies this constraint. While it can be argued that the ciphertexts belong to different block sizes, this immediately rules out ciphers like Playfair and Four-Square which operate on digraphs (Block Size = 2) . Further, both ciphers eliminate a single character (usually ‘j’) as part of the algorithm. Since our ciphertext contains 26 characters, we trivially eliminate these cipher schemes. 

It is far more difficult to rule out Hill Ciphers. This system relies on a n\times n matrix key where n is the size of the block. Here, it is possible to have different keys for each of the ciphertexts. Other than a series of frequency analysis tests for increasing block sizes, it seems far more efficient to try decoding the ciphers using n-gram correspondences. Attempting to identify repeating sequences of n-grams gives no discernable pattern. It is far more likely that our cipher is a polyalphabetic variant described below.


###	POLYALPHABETIC

Polyalphabetic ciphers use different alphabets in the encryption process to further diffuse letter frequencies and make decryption harder. In the other cryptographic schemes above, either single letters or blocks of letters map to the same letter or same block of letters regardless of their position in the text. Polyalphabetic ciphers provide a one-to-many or many-to-many relationship between letters which has far better security implications. One of the most popular ciphers in the polyalphabetic family is the Vigenère Cipher. This cipher Caesar shifts plaintext letters based on their position relative to a fixed keyword. The same plaintext character may appear at a different offset relative to the keyword and thus can map to several ciphertext characters. This property makes the Vigenère cipher incredibly resilient to frequency analysis. 

For longer messages, the keyword is repeated for the length of the message. Here lies the immediate weakness of the Vigenère Cipher. There are several attacks including Kasiski and Friedman which exploit this weakness. Once the key length, k, is discovered, the periodicity ensures that every kth element, i, is a Caesar Shift with parameter key_i.

Through the process of elimination, we have settled upon a polyalphabetic cipher for our unknown texts. However, running both the Kasiski and Friedman Index of Coincidence attacks does not give consistent results in determining the key length. Either we have made a mistake in our classification, or, the cipher we are dealing with does not have some constant period. There are variants of the Vigenère Cipher such as Autokey and Running-Key which remove some of the periodicity and render the above attacks unsuccessful (Practical Cryptography, 2017). In the next section, we discuss some variants of the Vigenère Cipher. In particular, we delay the discussion on Running-Key Ciphers since they are much more complex and require significantly more effort to analyze. We will leave such cipher as a last resort and discuss it in more detail in the related ciphers section along with modern Stream Ciphers (§5.2).

## VARIANTS OF THE VIGENÈRE CIPHER

### BEAUFORT

The Beaufort Cipher is quite similar to the classical Vigenère Cipher. Instead, encryption using this cipher is identical to decryption using Vigenère while decryption is equivalent to encryption. The cryptanalysis of the Beaufort Cipher is nearly identical to the cryptanalysis of the Vigenère Cipher. This involves finding the periodicity and uniformly applying a Caesar Shift across the letters in the same congruence class. Ultimately, our ciphers are not derived from this variant since this scheme preserves the key periodicity properties.

### AUTOKEY

The Vigenère variant of the Autokey Cipher is the first non-periodic polyalphabetic cipher that we have encountered. In this scheme, the key is extended in a way which does not introduce periodicity. Remember, a key must be extended for longer messages and memorizing long sequences of characters is very difficult. The Autokey Cipher meets this constraint by extending the key with another source of text which is derived from the message itself. There are mainly two variants of the Autokey Cipher, one which extends the key with plaintext and another which extends it through the ciphertext. The observant reader will notice, if the message is encoded with some key followed by the plaintext, how is it possible to decode ciphertext without the corresponding plaintext? The answer is the basis of many stream and block ciphers that use chaining methods. In these systems, the output of one computation is appended to the input of another. The autokey cipher first decodes the ciphertext on the key itself resulting in a series of plaintext characters. These characters are used to extend the key. While the ciphertext variant of the Autokey Cipher does not involve this step, it is much easier to decode. Simply, take the ciphertext and shift it at increasing offsets of the message to decode a large part of the plaintext message. The ciphertext variant was immediately discarded in this analysis since no offset of the ciphertext produced reasonable-looking English plaintext. The following section describes a weakness of the Autokey Cipher which was ultimately used to crack the encoded messages without knowledge of the key.

## WEAKNESSES OF THE AUTOKEY CIPHER

While the Autokey Cipher is much more secure than a simple Vigenère Cipher, its main weakness is that the plaintext is part of the key itself. Generally, when there exist components of an algorithm which are not random themselves, we introduce a potential weakness in the system. The keys in the autokey cipher are formed by appending the plaintext message to some chosen keyword of length k. We then truncate the last k characters of the plaintext to make the key as long as the message we are trying to encode. Having the key in the front gives enough padding so that we are not encoding the character with itself which would be almost trivial to crack. Knowing that there exists part of the plaintext in the key, we can simply try various fragments or “probes” into the ciphertext to decode other parts of the plaintext. This technique also provides information regarding the length of the initial keyword. 
Generally, the way to exploit this weakness is to select a word or phrase that is likely to be part of the plaintext message. Then we decode the ciphertext at offset position p. If the probe keyword is part of the plaintext message, we should start to uncover leading parts of the key itself. If the probe is longer than the length of the key, we will start to repeat segments of the probe in the plaintext which can give an indication to the length of the key. If no discernable plaintext is found at offset p, we can increment the offset or choose another probe to begin the attack.

More generally, smaller keys in almost all ciphers, produce weaker security guarantees. In the given ciphertexts, the keys are small enough to brute-force since they do not depend on information other than the initial keyword. Variant ciphers including the running-key cipher do not reuse the plain-text making an attack harder (§5.1).

## RESULTS

We were able to decode the plaintext message of the given ciphertexts using two approaches. In the first, we used the probing technique described in the section above. Using common words and phrases, we were able to extract fragments of the plaintext as well as the keyword used to seed the full key. A demonstration of this attack can be found in the source repository as a module written in the python language . The analyze_autokey.py script uses common English quadgrams to score each of the probe offsets. For a given probe, all possible partitions of the ciphertext are rotated with the probe keyword and scored to find the most likely plaintext fragments. Due to the way the decode function is written, this requires some manual effort to decode and stitch together the entire message. For the first ciphertext, the probe keyword “multitude” is tested against partitions of size 9 characters. The two highest and lowest scoring plaintext fragments are listed in the table below:

Table 4. Quadgram scores of plaintext fragments from autokey probing attack.

| Plaintext | Quadgram Score |
| --------- | -------------- |
| cesofthem | \-19.578       |
| emadetoog | \-26.535       |
| zuxujbfyl | \-65.152       |
| vzxlzxfwc | \-66.976       |

After a bit of trial-and-error we find the key length which produces the best plaintext message. This allows us to combine the probe with the generated message fragments to get the larger fragment “cesofthemultitudemadetoog”. Repeating this process along with trying different probes helps recover the entire message along with the key. The table below shows the plaintext recovery of all three ciphertexts.

Table 5. Plaintext recovery of ciphertexts encoded with autokey cipher.

|             |                                                          |
| ----------- | -------------------------------------------------------- |
| Ciphertext1 | xhhwpinevlgnfigpvafuvrotvylvyfxvvy...                    |
| Plaintext1  | idtheeveningbellissoundingthesunissettingforastrangew... |
|             |                                                          |
| Ciphertext2 | eatmrleiwwggtuidtargrjlalejgfaeqaskajiiajgfljjy...       |
| Plaintext2  | sagotherewasanemperorwhowassoexcessivelyfondo...         |
|             |                                                          |
| Ciphertext3 | ogkqyivrrxemwtsmkxhetojeahseehyglbjoowhol...             |
| Plaintext3  | atimetherewasalittleboywhohadtakencoldhehadgo...         |

While the attack described above is quite elegant, it is also quite time and labor intensive. The implementation of this attack is quite lacking in terms of features and optimizations. A more efficient implementation that uses elementary linear algebra instead of loops over all possible partitions has the potential to increase the rate of plaintext recovery. We are also limited by the quality of the initial probe. For longer messages, the same probe length requires far more partitions and consequently many more Quadgram calculations. Smaller keywords provide far less information and have higher rates of failure.  

To circumvent these issues, a brute-force implementation of the Autokey Cipher is also included in the source repository. As an input this method takes the size of the initial keyword and iterates over keys of this length. While a full brute-force solution would take as many as {26}^k iterations where k is the length of the key, our approach interjects and selects the best character one at a time, lowering the algorithmic complexity to linear time. For the ciphertexts above, the brute-force solution only took a couple seconds to find the correct plaintext given the key length. While the key length is not known beforehand, it is trivial to run through all key sizes up to some value K with this implementation.


## RELATED CIPHERS

### RUNNING-KEY CIPHER

The running-key cipher is a variant of the Vigenère and Autokey Ciphers. Like the Autokey Cipher, which attempts to minimize the periodic property of Vigenère keys, the running-key cipher renders the key-length finding Kasiski and Friedman IoC attacks useless. Unlike the Autokey cipher, the running-key cipher does not include part of the message into the key itself. As we have seen, simply guessing words or phrases which may be in the plaintext can reveals fragments of the key. Instead, the running-key cipher uses an unrelated text equal in length to the original message to encode. An additional few characters or blocks may be added unencrypted to the ciphertext to reference the alternative text, i.e. page numbers and offsets, used for the running-key. Generally, the unrelated text used in key-formation is part of some famous book or other written work. We can use common words and phrases to run a similar attack as the attack we used against the Autokey variant. In this case, however, we are likely to recover plaintext that may be part of either the original message or the key itself. This can introduce some interesting challenges in the cryptanalysis.

### STREAM CIPHER

Stream Ciphers are a modern variant that use the ideas of including the message in the key similar to the Autokey and Running-Key Cipher. Stream Ciphers are distinct in that they operate on single bits and digits rather than plaintext characters or strings. Generally, a plaintext bit is encrypted with a “running” key-stream and XOR with the previous bit. This also makes the stream cipher more akin to a one-time-pad (OTP), a cipher which theoretically removes all information from a given plaintext. With a random key-stream, this cipher has very good security properties. It is less used in practice due to the fact that it operates on single bits. While it is implementation dependent, for most applications it can be more efficient to work on large blocks such as those in AES, DES, and Feistel ciphers (Sharif & Mansoor, 2010).

## References

Lasry, G., Niebel, I., Kopal, N., & Wacker, A. (2017). Cryptanalysis of the Columnar Transposition Cipher with Long Keys. Cryptologia.

Norvig, P. (2012). English Letter Frequency Counts. Retrieved from norvig.com: https://norvig.com/mayzner.html

Practical Cryptography. (2017). Autokey Cipher. Retrieved from practicalcryptography.com: http://practicalcryptography.com/ciphers/autokey-cipher/

S.S.Dhenakaran, & Ilayaraja, M. (2012). Extension of Playfair Cipher using 16X16 Matrix. International Journal of Computer Applications.

Sharif, S. O., & Mansoor, S. (2010). Performance analysis of stream and block cipher algorithms. 2010 3rd International Conference on Advanced Computer Theory and Engineering (ICACTE).

Wikipedia. (2019). Index of Coincidence. Retrieved from wikipedia.org: https://en.wikipedia.org/wiki/Index_of_coincidence

Wikipedia. (2020). Caesar cipher. Retrieved from wikipedia.org: https://en.wikipedia.org/wiki/Caesar_cipher

