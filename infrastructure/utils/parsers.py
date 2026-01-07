import json
from datetime import datetime
from typing import Dict, Any, List


def parse_post_full_content_to_text(post_content: Dict[str, Any]) -> str:
    paragraphs = post_content.get("paragraphs", [])
    texts: List[str] = []
    for p in paragraphs:
        text = p.get("text")
        if text:
            texts.append(text.strip())

    return "\n\n".join(texts)


def parse_user_about_to_text(raw_about: str) -> tuple[Any, str]:
    if not raw_about:
        return None, ""

    try:
        data = json.loads(raw_about)
    except json.JSONDecodeError:
        return None, raw_about

    texts: List[str] = []

    def walk(nodes):
        for node in nodes:
            if "text" in node:
                texts.append(node["text"])
            if "children" in node:
                walk(node["children"])

    walk(data)

    return data, " ".join(texts).strip()


def get_miliseconds_since_epoch() -> int:
    current_date_time = datetime.now()
    milliseconds_since_epoch = int(current_date_time.timestamp() * 1000)

    return milliseconds_since_epoch


if __name__ == "__main__":
    sample_about = "[{\"children\":[{\"text\":\"I started Medium in November 2023.\"}]},{\"children\":[{\"text\":\"Here to share my progress and what works for me with transparency. \"}]},{\"children\":[{\"text\":\"My record would be earning over $10K on Medium within 13 months.\"}]},{\"children\":[{\"text\":\"Publication growing into 100K+ Followers within 16 months. \"},{\"text\":\"(due to all the writers and readers, of course)\",\"italic\":true}]},{\"children\":[{\"italic\":true,\"text\":\"Now I make $200 a Month, still a work in progress.\"}]},{\"children\":[{\"italic\":true,\"text\":\"Building connections and being helpful is a must.\"}]},{\"type\":\"paragraph\",\"children\":[{\"text\":\"My \",\"italic\":true},{\"type\":\"link\",\"url\":\"https://ko-fi.com/thebinjiang\",\"children\":[{\"text\":\"Ko-Fi\",\"italic\":true}]},{\"text\":\" link, but I prefer you come say hi to me on \",\"italic\":true},{\"type\":\"link\",\"url\":\"https://thebinjiang.substack.com/\",\"children\":[{\"text\":\"Substack\",\"italic\":true}]},{\"text\":\".\",\"italic\":true}]},{\"type\":\"paragraph\",\"children\":[{\"text\":\"Offering a free Medium account review for growth on \"},{\"type\":\"link\",\"url\":\"https://bin-jiang.kit.com/profile/products\",\"children\":[{\"text\":\"Kit.com\"}]},{\"text\":\" or on \"},{\"type\":\"link\",\"url\":\"https://thebinjiang.gumroad.com/\",\"children\":[{\"text\":\"Gumroad\"}]},{\"text\":\".\"}]},{\"children\":[{\"text\":\"Thanks for the Support.\\n\\n\\n\\n\"}]}]"
    result = parse_user_about_to_text(sample_about)
    print(result)

    sample_content = {
                    "__typename": "RichText",
                    "sections": [
                        {
                            "__typename": "Section",
                            "name": "7333",
                            "startIndex": 0,
                            "textLayout": None,
                            "imageLayout": None,
                            "videoLayout": None,
                            "backgroundImage": None,
                            "backgroundVideo": None
                        }
                    ],
                    "paragraphs": [
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_0",
                            "name": "ddee",
                            "href": None,
                            "text": "I Failed 47 System Design Interviews — Then One Netflix Engineer Changed Everything",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "H3",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_1",
                            "name": "9a0a",
                            "href": None,
                            "text": "A single shift in how I framed scalability turned rejection into three competing offers in thirty days.",
                            "iframe": None,
                            "layout": None,
                            "markups": [
                                {
                                    "__typename": "Markup",
                                    "name": None,
                                    "type": "STRONG",
                                    "start": 0,
                                    "end": 103,
                                    "href": None,
                                    "title": None,
                                    "rel": None,
                                    "anchorType": None,
                                    "userId": None,
                                    "creatorIds": None
                                }
                            ],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "H4",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_2",
                            "name": "4c0c",
                            "href": None,
                            "text": "From 47 rejections to 3 offers: the one question that turned my system design interviews around.",
                            "iframe": None,
                            "layout": "INSET_CENTER",
                            "markups": [],
                            "metadata": {
                                "__typename": "ImageMetadata",
                                "id": "1*ZT2SRcl-B_zZuZ0qC5EpxA.png",
                                "originalWidth": 1024,
                                "originalHeight": 1024,
                                "focusPercentX": None,
                                "focusPercentY": None,
                                "alt": None
                            },
                            "mixtapeMetadata": None,
                            "type": "IMG",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_3",
                            "name": "d975",
                            "href": None,
                            "text": "The whiteboard is blank. The marker is uncapped. The interviewer leans back and says design Twitter. And your brain just explodes into this mess of load balancers and microservices and Kafka streams because you think that’s what they want to hear. Two minutes in and you’re already lost in your own diagram.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_4",
                            "name": "c56b",
                            "href": None,
                            "text": "I did this forty seven times. Forty seven times I walked out thinking I nailed it, only to get the rejection email three days later. The polite kind. You know the one. “We’ve decided to move forward with other candidates.” Translation: you overthought it again.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_5",
                            "name": "0e45",
                            "href": None,
                            "text": "Here’s what nobody tells you about system design interviews. They’re not really testing if you know Redis or Cassandra or whatever the hot database is this month. Wait, let me back up. They ARE testing that, but that’s not why people fail. Most people fail because they’re performing. They’re trying to impress some imaginary staff engineer in the room instead of just solving the actual problem in front of them.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_6",
                            "name": "20a8",
                            "href": None,
                            "text": "I kept doing this thing where I’d jump straight to the complex solution. Sharding. Replication. Event sourcing. All the buzzwords. And the interviewer would just sit there nodding, taking notes, and I’d think I’m crushing this. Except I wasn’t. I was designing for a company that didn’t exist.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_7",
                            "name": "7895",
                            "href": None,
                            "text": "The Breaking Point",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "H3",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_8",
                            "name": "e167",
                            "href": None,
                            "text": "Interview thirty one. Fintech startup. Design a payment processing system. I’m drawing boxes and arrows and talking about database partitioning strategies and the guy stops me. Just stops me mid sentence. “How many transactions per second are we actually talking about here?”",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_9",
                            "name": "5590",
                            "href": None,
                            "text": "I froze. Because I had no idea. I’d been designing for a billion users when they had twelve thousand. Twelve thousand. You don’t need Kafka for twelve thousand users. You barely need a cache.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_10",
                            "name": "ce54",
                            "href": None,
                            "text": "That moment kept replaying in my head for weeks. Not because it was embarrassing, though it was. But because I suddenly saw the pattern. Every single interview, I was solving the wrong problem. I was designing systems for the scale I wanted to work at, not the scale that actually existed.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_11",
                            "name": "98ef",
                            "href": None,
                            "text": "It’s like when you’re learning to cook and you think you need every fancy ingredient and technique, but really you just need to know how to properly salt your pasta water. The basics done right beat complexity done wrong every single time.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_12",
                            "name": "9bb2",
                            "href": None,
                            "text": "The Conversation That Changed Everything",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "H3",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_13",
                            "name": "906d",
                            "href": None,
                            "text": "Three months into my rejection streak, I met Priya at a local tech meetup. She works at Netflix. I was venting, probably too much, and she just listened. Then she asked me one question. “What’s the first thing you ask in a system design interview?”",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_14",
                            "name": "b51f",
                            "href": None,
                            "text": "“Functional requirements?” I said.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_15",
                            "name": "803b",
                            "href": None,
                            "text": "She shook her head. “Ask what breaks if we do nothing.”",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_16",
                            "name": "9008",
                            "href": None,
                            "text": "That sentence rewired my entire brain. Because think about it. Every system starts as one server with one database. That’s it. Your job isn’t to avoid that starting point. Your job is to find the ONE thing that forces you to evolve beyond it. Too many reads? Okay, add a cache. Too many writes? Queue them. But only when you have to. Only when the current thing actually breaks.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_17",
                            "name": "0c29",
                            "href": None,
                            "text": "Wait, this connects to something else. I was reading this blog post about how Amazon built AWS, and Jeff Bezos had this rule. Start with the smallest thing that could work, then scale only the parts that are actually bottlenecks. Not the parts you think might become bottlenecks someday. The parts that are breaking right now, today.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_18",
                            "name": "8243",
                            "href": None,
                            "text": "When It Finally Clicked",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "H3",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_19",
                            "name": "4be7",
                            "href": None,
                            "text": "Interview forty eight. Logistics company. Design a package tracking system. I drew one box. One database. That’s it. Then I asked how many packages per day.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_20",
                            "name": "023f",
                            "href": None,
                            "text": "“About fifty thousand.”",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_21",
                            "name": "7efc",
                            "href": None,
                            "text": "“How many users checking statuses at the same time?”",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_22",
                            "name": "dce8",
                            "href": None,
                            "text": "“Maybe five thousand.”",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_23",
                            "name": "8f22",
                            "href": None,
                            "text": "I just sat there for a second. Thinking. Fifty thousand packages. Five thousand concurrent users. You know what that needs? One server. Maybe a read replica for the tracking queries. A simple cache for the packages people check most often. That’s it.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_24",
                            "name": "552c",
                            "href": None,
                            "text": "The interviewer was nodding but I could tell he was waiting for me to overcomplicate it. So I didn’t. I defended that simple design for like ten minutes. Explained why it would work. Where the actual bottlenecks would be. And THEN he said okay, what if we 10x overnight.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_25",
                            "name": "c656",
                            "href": None,
                            "text": "Now I added the queue. Now I talked about partitioning. But I’d earned it. I wasn’t guessing anymore. I was responding to an actual constraint.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_26",
                            "name": "82ea",
                            "href": None,
                            "text": "The offer came two days later. Then another one from a different company. Then another. Same approach every time. Start stupid simple. Defend it. Evolve only when forced.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_27",
                            "name": "eacd",
                            "href": None,
                            "text": "The Part Nobody Mentions",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "H3",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_28",
                            "name": "3345",
                            "href": None,
                            "text": "Here’s the nuance though. If you’re interviewing at Google or Meta or somewhere already operating at massive scale, starting small can look naive. These companies don’t have the luxury of “we’ll add a cache later.” They need you thinking about consensus algorithms and failure domains from minute one.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_29",
                            "name": "e2ae",
                            "href": None,
                            "text": "So you name the context upfront. You say given that you’re handling billions of requests, I’m assuming we start distributed. Should I focus on consistency trade offs or latency optimization first? You’re not showing off. You’re showing you understand that constraints dictate design.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_30",
                            "name": "d59a",
                            "href": None,
                            "text": "Also, if you don’t know something, just say it. I spent so many interviews bullshitting my way through questions about ZooKeeper or Raft or whatever. Just admit it. Then explain what you’d do to figure it out. That honesty lands so much better than the hand waving thing we all do.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_31",
                            "name": "972d",
                            "href": None,
                            "text": "What Actually Matters",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "H3",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_32",
                            "name": "d403",
                            "href": None,
                            "text": "System design interviews aren’t about knowing every database or caching layer that exists. They’re about knowing which question to ask first. What breaks if we do nothing? That one question unlocks everything else.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_33",
                            "name": "5edb",
                            "href": None,
                            "text": "Start with one box. One database. Defend it until the constraints force you to evolve. You’ll either discover the right design naturally, or you’ll discover the company doesn’t actually need the architecture they think they do.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_34",
                            "name": "e6d2",
                            "href": None,
                            "text": "Either way, you’ll sound like someone who’s built real systems. Because that’s how real systems actually get built. Not in some grand architectural vision at the start. But piece by piece, bottleneck by bottleneck, constraint by constraint.",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_35",
                            "name": "34a7",
                            "href": None,
                            "text": "What system design concept did you think you understood until an interview proved otherwise?",
                            "iframe": None,
                            "layout": None,
                            "markups": [],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        },
                        {
                            "__typename": "Paragraph",
                            "id": "66ba643865b1_36",
                            "name": "af0d",
                            "href": None,
                            "text": "Follow me for more such content.",
                            "iframe": None,
                            "layout": None,
                            "markups": [
                                {
                                    "__typename": "Markup",
                                    "name": None,
                                    "type": "EM",
                                    "start": 0,
                                    "end": 32,
                                    "href": None,
                                    "title": None,
                                    "rel": None,
                                    "anchorType": None,
                                    "userId": None,
                                    "creatorIds": None
                                }
                            ],
                            "metadata": None,
                            "mixtapeMetadata": None,
                            "type": "P",
                            "hasDropCap": None,
                            "dropCapImage": None,
                            "codeBlockMetadata": None
                        }
                    ]
                }
    result = parse_post_full_content_to_text(sample_content)
    print(result)