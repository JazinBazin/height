import xml.etree.ElementTree as ET


def addUrlToSiteMap(link, pk):
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse('sitemap.xml')
    urlset = tree.getroot()
    url = ET.SubElement(urlset, 'url', attrib={
        'pk': str(pk),
    })
    loc = ET.SubElement(url, 'loc')
    loc.text = link
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)


def removeUrlFromSiteMap(pk):
    pk = str(pk)
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse('sitemap.xml')
    urlset = tree.getroot()
    for url in urlset:
        if url.get('pk', -1) == pk:
            urlset.remove(url)
            break
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)
