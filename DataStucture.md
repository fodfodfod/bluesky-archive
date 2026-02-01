# Data Structure
All users will be referenced internally by their did to ensure data is kept with the right account, only converting to handle or display name when being shown to the user. 
```
user_data
├── add_list.txt
├── did:plc:thisistotallyarealdid
│   ├── posts.json
│   ├── user_data.json
│   ├── download_list.txt
│   └── embeds
        ├── image0.jpeg
│       └── image1.jpeg
└── did:plc:thisisadifferentuserwithnoimages
    ├── posts.json
    └── user_data.json

```
## posts.json
posts.json contains an array of dictionaries. Each dictionary will have one post and possibly a reply. These are based on the data returned by [app.bsky.feed.getAuthorFeed](https://docs.bsky.app/docs/api/app-bsky-feed-get-author-feed), which I think is based on the AT Protocol. Sample post:
```
    {
        "post": {
            "uri": "at://did:plc:nixzpkoldlyfbw36jcr42ybs/app.bsky.feed.post/3mdlpitgvl22f",
            "cid": "bafyreid6i27fdvvzeyq5enq6o2hpjmvyonrjtbuwwbqynt2qrh4wcff76e",
            "author": {
                "did": "did:plc:nixzpkoldlyfbw36jcr42ybs",
                "handle": "densinium.bsky.social",
                "displayName": "Densinium / Yuki",
                "avatar": "https://cdn.bsky.app/img/avatar/plain/did:plc:nixzpkoldlyfbw36jcr42ybs/bafkreibrl7sobueyfu4nb6pc7mppreil4mmsjamdbehxphpozrgvjdndcu@jpeg",
                "associated": {
                    "activitySubscription": {
                        "allowSubscriptions": "followers"
                    }
                },
                "labels": [],
                "createdAt": "2025-01-14T21:14:50.549Z"
            },
            "record": {
                "$type": "app.bsky.feed.post",
                "createdAt": "2026-01-29T21:16:09.615Z",
                "embed": {
                    "$type": "app.bsky.embed.images",
                    "images": [
                        {
                            "alt": "",
                            "aspectRatio": {
                                "height": 604,
                                "width": 474
                            },
                            "image": {
                                "$type": "blob",
                                "ref": {
                                    "$link": "bafkreid2lfdqjuyu6ehur7tya3wulx72x6knqjaedalzp4vwsbmwhjgnaa"
                                },
                                "mimeType": "image/jpeg",
                                "size": 142659
                            }
                        }
                    ]
                },
                "langs": [
                    "en"
                ],
                "text": "Plushie time"
            },
            "embed": {
                "$type": "app.bsky.embed.images#view",
                "images": [
                    {
                        "thumb": "https://cdn.bsky.app/img/feed_thumbnail/plain/did:plc:nixzpkoldlyfbw36jcr42ybs/bafkreid2lfdqjuyu6ehur7tya3wulx72x6knqjaedalzp4vwsbmwhjgnaa@jpeg",
                        "fullsize": "https://cdn.bsky.app/img/feed_fullsize/plain/did:plc:nixzpkoldlyfbw36jcr42ybs/bafkreid2lfdqjuyu6ehur7tya3wulx72x6knqjaedalzp4vwsbmwhjgnaa@jpeg",
                        "alt": "",
                        "aspectRatio": {
                            "height": 604,
                            "width": 474
                        }
                    }
                ]
            },
            "bookmarkCount": 0,
            "replyCount": 0,
            "repostCount": 2,
            "likeCount": 21,
            "quoteCount": 0,
            "indexedAt": "2026-01-29T21:16:16.654Z",
            "labels": []
        }
    },
```
## user_data.json
user_data.json stores extra info about a user. It pulls from [app.bsky.actor.getProfile](https://docs.bsky.app/docs/api/app-bsky-actor-get-profile). It is stored as an array and everytime a request is performed the new data is appended. 
## add_list.txt
add_list.txt is a list of users to add to the archiver. Each line should be one user, either a did or handle. Comment lines start with `#`
## download_list.txt
download_list.txt contains that images that need to be download for that user
