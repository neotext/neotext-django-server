from neotext.lib.neotext_quote_context.quote import Quote

t1 = Quote (
    citing_quote="one does not live by bread alone, "
    "but by every word that comes from the mouth of the Lord",
    citing_url='http://www.neotext.net/demo/',
    cited_url='https://www.biblegateway.com/passage/?search=Deuteronomy+8&amp;version=NRSV'
)

t1.hash() = '32b19d9333fff69d16d5bf89bc1eb76f6b39eb58'
t1.data()['citing_context_before'] = 'ted texts on biblegateway.com; and the Al Gore example referenced an article on the washingtonpost.com. Using Neotext allows the reader to more easily make the intertextual connections between the two verses, without having to leave the current page. How the Neotext Quote-Context Service Works The example I’ve given you is made possible through a WordPress Plugin that operates on the html <blockquote> tag: <blockquotecite=”https://www.biblegateway.com/passage/?search=Deuteronomy+8&version=NRSV”>'
t1.data()['citing_context_after'] = '</blockquote> As part of the wordpress saving process, the WordPress Plugin submits the url of the post to the Neotext Web Service, which looks up the surrounding context of each quote and creates json files for each citation. Each quote’s citation file is uploaded to Amazon S3 for later retreival by the client. On the client side, the Neotext custom jQuery library: uses the url from each blockquote “cite” attribute and the quote hashes the url and quote text looks up the previously generated json from the hash: http://read.neotext.net/quote/sha1/0.02/32/32b19d9333fff69d16d5bf89bc1eb76f6b39eb58.json injects the content from the json fields into hidden divs, which are made visible when the user clicks the arrows or link: Code Example: The code for displaying the looked-up information is part of a free open source jQuery plugin called neotext-quote-context.js, available as a wordpress or jQuery plugin. Get simplified html source of this page Download neotext-sample.html (view online) Sav'


t2 = Quote(
 citing_quote="I took the initiative in creating the Internet.",
 citing_url="http://www.neotext.net/demo/"
 cited_url="https://www.washingtonpost.com/news/fact-checker/wp/2013/11/04/a-cautionary-tale-for-politicians-al-gore-and-the-invention-of-the-internet/"
)
