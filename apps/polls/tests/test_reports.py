

# # in-memry copy PDF file
# buffer_file = io.BytesIO()
# buffer_file.write(response.getvalue())
# parser = PDFParser(buffer_file)
# doc = PDFDocument(parser)
# info = doc.info[0]

# self.assertEqual(info['Title'], b'Report about polls')
# self.assertEqual(info['Subject'], b'Polls')
# self.assertEqual(info['Creator'], settings.SITE_NAME.encode())
# self.assertEqual(info['Keywords'], b'Polls, votes, voters')
# self.assertEqual(info['Author'], self.active_superuser.get_full_name().encode())

# from PyPDF2 import PdfFileReader
# doc = PdfFileReader('/home/wlysenko/Downloads/Report about polls 2016-08-18 13-14-11.pdf')
# print('Pages:', doc.getNumPages())
# doc.getDocumentInfo()
