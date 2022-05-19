## get Methods available:
## curl -s --data "<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName><params><param><value><string/></value></param></params></methodCall>" http://${WORDPRESS_SITE}/xmlrpc.php
##

WORDPRESS_SITE="www.dhqhrtnwl.shop"

for i in system.multicall system.listMethods system.getCapabilities demo.addTwoNumbers demo.sayHello pingback.extensions.getPingbacks pingback.ping wp.restoreRevision wp.getRevisions wp.getPostTypes wp.getPostType wp.getPostFormats wp.getMediaLibrary wp.getMediaItem wp.getCommentStatusList wp.newComment wp.editComment wp.deleteComment wp.getComments wp.getComment wp.setOptions wp.getOptions wp.getPageTemplates wp.getPageStatusList wp.getPostStatusList wp.getCommentCount wp.deleteFile wp.uploadFile wp.suggestCategories wp.deleteCategory wp.newCategory wp.getTags wp.getCategories wp.getAuthors wp.getPageList wp.editPage wp.deletePage wp.newPage wp.getPages wp.getPage wp.editProfile wp.getProfile wp.getUsers wp.getUser wp.getTaxonomies wp.getTaxonomy wp.getTerms wp.getTerm wp.deleteTerm wp.editTerm wp.newTerm wp.getPosts wp.getPost wp.deletePost wp.editPost wp.newPost wp.getUsersBlogs; do echo -e "\n==\n MethodCall: $i\n $(date)\n"; curl -s --data "<?xml version="1.0"?><methodCall><methodName>$i</methodName><params><param><value><string/></value></param></params></methodCall>" https://${WORDPRESS_SITE}/xmlrpc.php; sleep 2s; done

##
## add to /etc/apache2/apache2.conf before any "Include "-Statements
##
## <Files xmlrpc.php>
##     Deny from all
##     Satisfy all
## </Files>
##
## maybe you want to add something like 
##
## ErrorDocument 403 https://twitter.com/intent/tweet?text=maaan!%20i%20am%20so%20fucking%20lame
##
