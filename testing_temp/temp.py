from summarizer import Summarizer,TransformerSummarizer
from transformers import logging

logging.set_verbosity_error()
body = '''
The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price.
The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal.
Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008.
Real estate firm Tishman Speyer had owned the other 10%.
The buyer is RFR Holding, a New York real estate company.
Officials with Tishman and RFR did not immediately respond to a request for comments.
It's unclear when the deal will close.
The building sold fairly quickly after being publicly placed on the market only two months ago.
The sale was handled by CBRE Group.
The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building.
The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028.
Meantime, rents in the building itself are not rising nearly that fast.
While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities.
Still the building is among the best known in the city, even to people who have never been to New York.
It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top.
It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day.
The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices.
Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest.
Blackstone Group (BX) bought it for $1.3 billion 2015.
The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself.
Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete.
Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title.
'''
# model = Summarizer()

# body="रांची. झारखंड में 62000 से अधिक पारा शिक्षकों को मुख्यमंत्री हेमंत सोरेन ने बड़ा गिफ्ट दिया है. शिक्षकों को ईपीएफ का लाभ देने के फैसले पर मुहर लग गई है. इसके लिए पारा शिक्षकों की सेवा शर्त नियमावली को स्वीकृति दी गई है. नियमावली को स्वीकृति मिलने के बाद अब पारा शिक्षक अब सहायक अध्यापक कहलाएंगे. पारा शिक्षकों को मिलने वाले ईपीएफ लाभ की बात करें तो इनके मानदेय से छह फीसदी राशि कटेगी. जबकि छह फीसदी राशि राज्य सरकार देगी. पारा शिक्षकों की सेवाशर्त नियमावली का प्रस्ताव राज्य के स्कूली शिक्षा एवं साक्षरता विभाग ने तैयार किया है. जिस पर वित्त विभाग ने अनापत्ति दे दी है.पारा शिक्षकों की सेवाशर्त नियमावली बनने के बाद अब वे न सिर्फ सहायक अध्यापक कहे जाएंगे बल्कि उनके मानदेय में भी वृद्धि होगी. शिक्षक पात्रता परीक्षा पास पारा शिक्षकों के मानदेय में 50 फीसदी की वृद्धि होगी, वहीं सिर्फ प्रशिक्षित पारा शिक्षकों के मानदेय में 40 फीसदी का इजाफा होगा. ऐसे में पहली से पांचवीं में पढ़ाने वाले प्रशिक्षित पारा शिक्षक (सहायक अध्यापक) को 4800 रुपये का मानदेय बढ़ने के बाद 1008 रुपये ईपीएफ के लिए अंशदान के रूप में देना होगा. वहीं, छठी से आठवीं के सिर्फ प्रशिक्षित पारा शिक्षकों को 1092 रुपये देने होंगे."

model = TransformerSummarizer(transformer_type="Bert",transformer_model_key="bert-base-uncased")

# result = model(body, ratio=0.2)  # Specified with ratio
# result = model(body, min_length=70)  # Specified with ratio
result = model(body, num_sentences=2)  # Will return 3 sentences 

print(result)

# 1. ablert  transformer_type="Albert",transformer_model_key="albert-base-v2"
# The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. 
# Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which 
# was formerly known as Sears Tower, once the world's tallest.

# 2. XLNet transformer_type="XLNet",transformer_model_key="xlnet-large-cased"
# The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. 
# The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal.

# 3. roberta   transformer_type="Roberta",transformer_model_key="roberta-large"
# The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. 
# Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which 
# was formerly known as Sears Tower, once the world's tallest.

# 4. BigBird  transformer_type="BigBird",transformer_model_key="google/bigbird-roberta-base"
# The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. 
# The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building.

# 5. xlm transformer_type="XLM",transformer_model_key="xlm-mlm-en-2048"
# The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. 
# Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which 
# was formerly known as Sears Tower, once the world's tallest.

# 6. GPT2  transformer_type="GPT2",transformer_model_key="gpt2-large"
# The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. 
# Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which 
# was formerly known as Sears Tower, once the world's tallest.

#7. Bert transformer_type="Bert",transformer_model_key="bert-base-uncased"
# The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. 
# The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building.
