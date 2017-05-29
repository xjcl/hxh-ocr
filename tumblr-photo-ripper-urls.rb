# modified from source:  https://gist.github.com/jamiew/1080846

# Usage:
#   [sudo] gem install mechanize
#   ruby tumblr-photo-ripper.rb

require 'rubygems'
require 'mechanize'

# Your Tumblr subdomain, e.g. "jamiew" for "jamiew.tumblr.com"
site = "hxh-textposts"
FileUtils.mkdir_p(site)

# putting a value more than 1 messes up our stdout output !
num = 50
start = 0

loop do
  url = "http://#{site}.tumblr.com/api/read?type=photo&num=#{num}&start=#{start}"
  page = Mechanize.new.get(url)
  doc = Nokogiri::XML.parse(page.body)

  images = (doc/'post photo-url').select{|x| x if x['max-width'].to_i == 1280 }
  image_urls = images.map {|x| x.content }

  image_urls.each do |url|
    puts "#{url}"
  end

  if images.count < num
    break
  else
    start += num
  end

end
