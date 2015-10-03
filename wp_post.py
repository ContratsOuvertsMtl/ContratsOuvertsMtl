from wordpress_xmlrpc import *
from wordpress_xmlrpc.methods.posts import *
from wordpress_xmlrpc.methods.users import *

wp = Client('https://bluehost.com/xmlrpc.php', 'pascalrobichaud.org', 'password')


wp.call(GetPosts())

wp.call(GetUserInfo())

post = WordPressPost()
post.title = 'My new title'
post.content = 'This is the body of my new post.'
post.terms_names = {
  'post_tag': ['test', 'firstpost'],
  'category': ['Introductions', 'Tests']
}
wp.call(NewPost(post))
