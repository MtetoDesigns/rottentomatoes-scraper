## Selectors: 

x path: 

All items: //div[@class="flex-container"]

Name:       //span[@class="p--small"]
Tomatoes_score:   //rt-text[@slot="criticsScore"]
Popcorn_score:    //rt-text[@slot="audienceScore"]
Date:       //span[@class="smaller"]

Load more: //div[@class="discovery__actions"]/button

CSS:

// All items
const allItems = 'div.flex-container';

// Name
const name = 'span.p--small';

// Tomatoes_score
const tomatoes = 'rt-text[slot="criticsScore"]';

// Popcorn_score
const popcorn = 'rt-text[slot="audienceScore"]';

// Date
const date = 'span.smaller';

// Load more button
const loadMore = 'div.discovery__actions > button';
