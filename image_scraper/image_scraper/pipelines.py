# # -*- coding: utf-8 -*-

# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

# class ImageScraperPipeline(ImagesPipeline):
    
#     def set_filename(self, response):
#     	return 'full/{0}.jpg'.format(response.meta['title'][0])

#     def get_media_requests(self, item, info):
#     	for image_url in item['image_urls']:
#     		yield scrapy.Request(image_url, meta={'title': item['title']})

#    	def get_images(self, response, request, info):
#    		# This function is overriding get_images fucntion in ImagesPipeline
#    		for key, image, buf in super(ImageScraperPipeline, self).get_images(response, request, info):
#    			key = 	self.set_filename(response)
#    		yield key, image, buf
class ImageScraperPipeline(ImagesPipeline):

    #Name download version
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    #Name thumbnail version
    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = thumb_id + request.url.split('/')[-1]
        return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

    def get_media_requests(self, item, info):
        #yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        for image in item['image_urls']:
            yield scrapy.Request(image)