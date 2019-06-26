import xml.etree.ElementTree as ET

sitemap_file_name = 'sitemap.xml'


def addUrlToSiteMap(link, pk):
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse(sitemap_file_name)
    urlset = tree.getroot()
    url = ET.SubElement(urlset, 'url', attrib={
        'pk': str(pk),
    })
    loc = ET.SubElement(url, 'loc')
    loc.text = link
    tree.write(sitemap_file_name, encoding='UTF-8', xml_declaration=True)


def removeUrlFromSiteMap(pk):
    pk = str(pk)
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse(sitemap_file_name)
    urlset = tree.getroot()
    for url in urlset:
        if url.get('pk', -1) == pk:
            urlset.remove(url)
            break
    tree.write(sitemap_file_name, encoding='UTF-8', xml_declaration=True)
