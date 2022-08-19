from prodconsumer import Producer, Consumer
import unittest

class TestProducer(unittest.TestCase):

    def test_success_fetch_url(self):
        task = Producer().fetch_url("https://www.google.com")
        res = task.status_code
        self.assertEqual(res, 200)


#     def test_fail_fetch_url(self):
#         task = Producer().fetch_url.s("fail.fail").delay()
#         res = task.get()
#         self.assertEqual(res, None)
#         self.assertEqual(task.status, 'SUCCESS')

# class TestConsumer(unittest.TestCase):

#     def test_success_fetch_url(self):
#         task = Consumer().extract_hyperlink.s("https://www.google.com").delay()
#         res = task.get()
#         self.assertEqual(res, "https://www.google.com - 200")
#         self.assertEqual(task.status, 'SUCCESS')

#     def test_fail_fetch_url(self):
#         task = Producer().fetch_url.s("fail.fail").delay()
#         res = task.get()
#         self.assertEqual(res, None)
#         self.assertEqual(task.status, 'SUCCESS')

if __name__ == '__main__':
    unittest.main()