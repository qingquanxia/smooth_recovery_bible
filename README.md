# Recovery Bible formatting project

The original Recovery-Version Bible is separated into verses, and all the verses are capitalized. There are no paragraphs. Besides verses, the only other structure is the poetical line break, which is indicated by a forward slash. If you look at the HTML of https://text.recoveryversion.bible/01_Genesis_4.htm, for example, each poetical line of Genesis 4:23-24 is preceded by either a <span class="acolon" /> or <span class="bcolon" /> tag. Hence, these span tags indicate the beginning of a new line. (By the way, I don't know the difference between acolon and bcolon.)

When making a smooth version of the Bible, there are hence two things I must consider.
The first is that to remove verse numbers, I must fix the capitalization between the verses. I call this fixing "verse boundaries." This is very straightforward in many cases, like when the previous verse ends in a period, or the current verse begins with a name, etc. However, there are also many cases which require considerably more judgment.
The second is to keep the poetical line structure intact, even after we have removed the verses.

Rules:
(1) Verses that follow immediately after a period or question mark are always capitalized. Note that this policy might not be so good for question marks (here are the counter-examples found in the interior of verses: (Exodus 3:13, Exodus 13:14, Judges 4:20, 2Samuel 3:12, 2Kings 7:19, Proverbs 31:2, Jeremiah 5:19, Jeremiah 7:19, Jeremiah 18:6, Jeremiah 23:24, Jeremiah 23:28, Jeremiah 23:33, Jeremiah 23:35, Jeremiah 23:37, Jeremiah 30:21, Jeremiah 35:13, Ezekiel 21:13, Haggai 1:9, Zechariah 8:6, Malachi 1:6, Malachi 1:8, Malachi 1:9, Malachi 1:13, Matthew 6:31, Matthew 6:31, Matthew 12:10, Matthew 27:46, Mark 11:3, Mark 15:34, John 4:27, John 21:12, Acts 7:35, Romans 3:8)). However, there are so many verses that end with question marks that it would take a long time to check all of them, and most of the words after question marks in verse boundaries
(2) Any word after a <span class="(a/b)colon"/> is capitalized, as it indicates we are in the line of a poetic section.
(3) Words after colons are handled on a case by case basis. In many cases, these are lowercased, but there are a few exceptions. Where there are precedents, I have referenced them in making my decision, and where there is no precedent, I've marked them as ambiguous.
(4) Words after em-dashes are usually lowercased. The one exception
(5) Verses after a verse containing <span>
(6) If the previous word ends with a semi-colon, comma, or nothing at all, we lowercase it unless the verse begins with a name, or pronoun of God, or the start of a quotation

Assertions:
(1) Only the capitalization of the words have been changed. No actual letter has been changed.
(2) Only the beginning letter of each verse has been changed. None of the interior has changed at all.




# Random notes:


Bible capitalization:
6/16/21: got through Gen1 to Gen36
6/17/21: got through Gen37 to Gen50 (that is, finished Genesis). Today I decided going through all the verses would be too slow, since most verses end in periods or questions anyway, so I can write a program to find verses which don't end in periods or questions.
5/20/22:



REMEMBER:
- properly change "Who" back to "who" to be consistent with rest of text. --------- Done for both OT and NT, 5/29/22
- check the endings of chapters for punctuation, just in case. --------- Done for both OT and NT, 5/29/22
- go back and handle /<span> stuff. Also, we have not touched the "poetry" books (Job, Psalms, Proverbs, SS, Isaiah, Jeremiah, Lamentations, Hosea, Joel, Amos, Obadiah, Micah, Nahum, Habakkuk, Zephaniah), although there are some sections without /<spans>'s, like Isaiah 6 ------------ update (5/29/22) we've now handled all the "poetry" books as well.
- Found errors in Mechron version of (Gen 32, Exo 8, Exo 20) in verse numbering. Fixed them on local copy.
- The following are tricky verses: Eph 4:4, 2Timothy 4:2, Titus 1:5, 1Peter 5:1, Rev 7:4, Rev 18:11, Rev 21:12,
- Reference verses: 1Timothy 3:1, 2Timothy 2:11, Titus 2:7, Heb 8:1, Heb 12:20, 2Peter 1:17, 2Peter 2:22, 1John 4:2, Rev 17:10
- See Acts 7:35 for a verse which has a non-capitalized word after the question mark.

- handle <br> elements (see Gen 4)
- make sure the boundary between span and non-span are properly capitalized.
- check Isaiah 8:19 (em dashes in particular) ----------------- Done 7/10/22, capitalized: see 1Cor 9:15, There is no example within a verse, other than (Daniel 5:27,28, 1Cor 9:15).
- check Amos 9:12

ASSERTIONS:
- all words after <span> are capitalized ------------- Done for OT 5/29/22, in NT, the only verse with spans in it is 1 Timothy 3:16
- every book has at least one lowercase verse (go back and check Philemon in particular) -------- Done: Philemon lowercased and assertion checked (only a few poetry books don't have lowercase verses, namely Psalms, Proverbs, SongofSongs, Lamentations, Hosea, Joel, Obadiah, Micah, Nahum, Habakkuk, Zephaniah) 7/10/22
- the interior of verses have not been modified.
