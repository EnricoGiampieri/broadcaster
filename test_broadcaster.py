import unittest
import itertools as it
import sys
import re

from broadcaster import BroadCaster

class BroadcasterTest(unittest.TestCase):
    def setUp(self):
        self.lista = [1, 2, 3, 4]
        self.BC = BroadCaster(self.lista)
        
    def testToList(self):
        self.assertTrue(self.lista == list(self.BC))
        self.assertTrue( list(self.BC) == self.BC.BClist() )
        
    def testToSet(self):
        self.assertTrue(self.lista==list(set(self.BC)))
        self.assertTrue( set(self.BC) == self.BC.BCset() )
        
        
class MapFilterTest(unittest.TestCase):
    def setUp(self):
        self.lista = [1, 2, 3, 4]
        self.BC = BroadCaster(self.lista)
        
    def testMapFilter1(self):
        self.res = self.BC.BCmapfilter()
        self.assertTrue( self.res.BClist() == [1, 2, 3, 4] )
        
    def testMapFilter2(self):    
        self.res = self.BC.BCmapfilter(None,None)
        self.assertTrue( self.res.BClist() == [1, 2, 3, 4] )
        
    def testMapFilter3(self):    
        self.res = self.BC.BCmapfilter(lambda i:i*2 ,None)
        self.assertTrue( self.res.BClist() == [2, 4, 6, 8] )
        
    def testMapFilter4(self):    
        self.res = self.BC.BCmapfilter(filter=lambda i: i<4)
        self.assertTrue( self.res.BClist() == [1, 2, 3] )
        
    def testMapFilter5(self):    
        self.res = self.BC.BCmapfilter(lambda i:i**2 ,lambda i: i<4)
        self.assertTrue( self.res.BClist() == [1, 4, 9] )
    
    def testMapFilter6(self): 
        self.res = self.BC
        self.assertRaises(TypeError, self.BC.BCmapfilter(1 ,None).BClist)
        
    def testMapFilter7(self): 
        self.res = self.BC
        self.assertRaises(TypeError, self.BC.BCmapfilter(None ,1).BClist)
        
    def testMapFilter8(self): 
        self.res = BroadCaster(['doglet','dog','purdog']).BCmapfilter( lambda i:re.sub('dog','cat',i) ).BClist()
        self.assertTrue( self.res == ['catlet', 'cat', 'purcat'])
        self.res = BroadCaster([])
        
    def tearDown(self):
        self.assertTrue(isinstance(self.res,BroadCaster))
        
        
class ReduceTest(unittest.TestCase):
    def setUp(self):
        self.lista = [1, 2, 3, 4, 4]
        self.BC = BroadCaster(self.lista)
    
    def testReduce1(self):
        self.res = self.BC.BCpairwise(lambda i,j: i+j)
        self.assertTrue( self.res.BClist() == [3, 5, 7, 8] )
        
    def testReduce2(self):
        self.res = self.BC.BCpairwise(lambda i,j: i+j, None)
        self.assertTrue( self.res.BClist() == [3, 5, 7, 8] )
        
    def testReduce3(self):
        self.res = self.BC.BCpairwise(lambda i,j: i+j, 0)
        self.assertTrue( self.res.BClist() == [1, 3, 5, 7, 8] )
        
    def testReduce4(self):
        self.res = self.BC.BCpairwise(lambda i,j: i+j, 3)
        self.assertTrue( self.res.BClist() == [4, 3, 5, 7, 8] )
        
    def testReduce5(self):
        self.res = self.BC.BCpairwise(lambda i,j,: i+j, accumulate=True)
        self.assertTrue( self.res.BClist() == [3, 6, 10, 14] )
        
    def testReduce6(self):
        self.res = self.BC.BCpairwise(lambda i,j,: i+j, 5, accumulate=True)
        self.assertTrue( self.res.BClist() == [6, 8, 11, 15, 19] )
        
    def tearDown(self):
        self.assertTrue(isinstance(self.res,BroadCaster))
        
        
class ApplyTest(unittest.TestCase):
    def setUp(self):
        self.lista = 'babbo'
        self.BC = BroadCaster(self.lista)
        
    def testApply1(self):
        self.res = self.BC.BCapply(enumerate)
        self.assertTrue( self.res.BClist() == [(0, 'b'), (1, 'a'), (2, 'b'), (3, 'b'), (4, 'o')] )
        
    def testApply2(self):
        self.res = self.BC.BCapply(enumerate, 2)
        self.assertTrue( self.res.BClist() == [(2, 'b'), (3, 'a'), (4, 'b'), (5, 'b'), (6, 'o')] )
        
    def testApply3(self):
        self.res = self.BC.BCapply(it.groupby)
        res = list( (i[0],list(i[1])) for i in self.res)
        self.assertTrue( res == [('b', ['b']), ('a', ['a']), ('b', ['b', 'b']), ('o', ['o'])] )
        
    def testApply4(self):
        self.res = self.BC.BCapply(it.izip, xrange(5))
        self.assertTrue( self.res.BClist() == [('b', 0), ('a', 1), ('b', 2), ('b', 3), ('o', 4)] )
        
    def testApply5(self):
        self.res = self.BC.BCapply(it.groupby)
        res = list( (i[0],list(i[1])) for i in self.res)
        self.assertTrue( res == [('b', ['b']), ('a', ['a']), ('b', ['b', 'b']), ('o', ['o'])] )
        
    def tearDown(self):
        self.assertTrue(isinstance(self.res,BroadCaster))
        
        
class EmergeTest(unittest.TestCase):
    def setUp(self):
        self.lista = 'aiuole'
        self.BC = BroadCaster(self.lista)
        
    def testEmerge1(self):
        self.res = self.BC.upper()
        self.assertTrue( self.res.BClist() == ['A','I','U','O','L','E'] )
    
    def testEmerge2(self):
        self.res = self.BC.__add__('a')
        self.assertTrue( self.res.BClist() == ['aa', 'ia', 'ua', 'oa', 'la', 'ea'] )
        
    def testEmerge3(self):
        self.res = BroadCaster([int,float,complex])(1)
        self.assertTrue( self.res.BClist() == [1, 1.0, (1+0j)] )
    
    def tearDown(self):
        self.assertTrue(isinstance(self.res,BroadCaster))

        
class FlattenTest(unittest.TestCase):
    def testFlatten1(self):
        lista = [[0,1,2],[3,4],[5,6],7]
        self.res = BroadCaster(lista).BCflatten()
        self.assertTrue( self.res.BClist() == range(8) )
        self.assertTrue(isinstance(self.res,BroadCaster))
        
    def testFlatten2(self):
        lista = range(8)
        self.res = BroadCaster(lista).BCflatten()
        self.assertTrue( self.res.BClist() == range(8) )
        self.assertTrue(isinstance(self.res,BroadCaster))
        
    def testFlatten3(self):
        lista = [[[1,2,3]],3]
        self.res = BroadCaster(lista).BCflatten()
        self.assertTrue( self.res.BClist() == [[1,2,3],3] )
        self.assertTrue(isinstance(self.res,BroadCaster))

        
class SplitTest(unittest.TestCase):
    def setUp(self):
        lista = [[1,2],[3,4],[5,6],[7,8]]
        self.BC = BroadCaster(lista)
        
    def testSplit1(self):
        self.res = self.BC.BCsplit(0).BClist()
        self.assertTrue(self.res == [1,2,3,4,5,6,7,8 ] )
        
    def testSplit2(self):
        self.res = self.BC.BCsplit(1).BClist()
        self.assertTrue(self.res == [[1],[2],[3],[4],[5],[6],[7],[8] ] )
        
    def testSplit3(self):
        self.res = self.BC.BCsplit(4).BClist()
        self.assertTrue(self.res == [[1,2,3,4],[5,6,7,8] ] )
        
    def testSplit4(self):
        self.res = self.BC.BCsplit(3).BClist()
        self.assertTrue(self.res == [[1,2,3],[4,5,6] ] )
        
    def testSplit5(self):
        self.res = self.BC.BCsplit(3,fillvalue=-1).BClist()
        self.assertTrue(self.res == [[1,2,3],[4,5,6],[7,8,-1] ] )
        
    def testSplit6(self):
        self.res = self.BC.BCsplit(3,fillvalue=None).BClist()
        self.assertTrue(self.res == [[1,2,3],[4,5,6],[7,8,None] ] )
        
        
class GetTest(unittest.TestCase):
    def setUp(self):
        lista = [[1,2],[3,4],[5,6],[7,8]]
        self.BC = BroadCaster(lista)
        
    def testGet1(self):
        self.res = self.BC[0]
        self.assertTrue( self.res.BClist() == [1,3,5,7] )
        
    def testGet2(self):
        self.res = self.BC[::-1]
        self.assertTrue( self.res.BClist() == [[2,1],[4,3],[6,5],[8,7]] )
        
    def testGet3(self):
        self.res = self.BC[[1,0,1]]
        self.assertTrue( self.res.BClist() == [[2,1,2],[4,3,4],[6,5,6],[8,7,8]] )
        
    def tearDown(self):
        self.assertTrue(isinstance(self.res,BroadCaster))
    
    
class WritableObject:
    def __init__(self):
        self.content = ""
    def write(self, string):
        self.content += string  
    

class FormatTest(unittest.TestCase):
    def setUp(self):
        self.BC = BroadCaster([1,2,3,3.1415,5.7])
        self.out = WritableObject()
        
    def testFormat1(self):
        self.res = self.BC.BCformat(stdout=self.out).BClist()
        self.assertTrue( self.out.content == "1 2 3 3.1415 5.7" )
        
    def testFormat2(self):
        self.res = self.BC.BCformat("{}"," ",self.out).BClist()
        self.assertTrue( self.out.content == "1 2 3 3.1415 5.7" )
        
    def testFormat3(self):
        self.res = self.BC.BCformat("{}",", ",self.out).BClist()
        self.assertTrue( self.out.content == "1, 2, 3, 3.1415, 5.7" )
        
    def testFormat4(self):
        self.res = self.BC.BCformat("{:.3f}",", ",self.out).BClist()
        self.assertTrue( self.out.content == "1.000, 2.000, 3.000, 3.142, 5.700" )

        
class TransposeTest(unittest.TestCase):
    def testTranspose1(self):
        lista = [[1,1,1,1],[2,2,2,2]]
        self.BC = BroadCaster(lista)
        self.res = self.BC.BCtranspose().BClist()
        self.assertTrue( self.res == [[1,2],[1,2],[1,2],[1,2]] )
        
    def testTranspose2(self):
        lista = [[1,1,1],[2,2,2,2]]
        self.BC = BroadCaster(lista)
        self.res = self.BC.BCtranspose().BClist()
        self.assertTrue( self.res == [[1,2],[1,2],[1,2]] )
        
    def testTranspose3(self):
        lista = [[1,1,1],[2,2,2,2]]
        self.BC = BroadCaster(lista)
        self.res = self.BC.BCtranspose(fillvalue=None).BClist()
        self.assertTrue( self.res == [[1,2],[1,2],[1,2],[None,2]] )
        
    def testTranspose4(self):
        lista = [[1,1,1],[2,2,2,2]]
        self.BC = BroadCaster(lista)
        self.res = self.BC.BCtranspose(fillvalue=-2).BClist()
        self.assertTrue( self.res == [[1,2],[1,2],[1,2],[-2,2]] )
     
        
#class RegexTest(unittest.TestCase):
#    def setUp(self):
#        self.lista = [ 'repeat 1234', 'my name if BroadCaster', "i like dogs, but when i don't like digs"  ]
#        self.BC = BroadCaster(self.lista)
#        
#    def testRegex1(self):
#        regex = r"(\b.+pea.+\b)"
#        self.res = self.BC.BCregex(regex).BClist()
#        print self.res
#        self.assertTrue( self.res == [('repeat',)] )
  
    
class SubTest(unittest.TestCase):
    def setUp(self):
        self.lista = [['a','b','c'],['me','you','he','her','it']]
        self.BC = BroadCaster(self.lista)
        
    def testSub0(self):
        """fail if you call a method meant for the subelements"""
        self.assertRaises(AttributeError, self.BC.upper().BClist)
        
    def testSub1(self):
        """can emerge it with the appropriate method"""
        self.res = self.BC.BCsub( 'upper' ).BClist()
        self.assertTrue( self.res == [['A','B','C'],['ME','YOU','HE','HER','IT']] )
        
    def testSub2(self):
        self.res = self.BC.BCsub( 'BCmapfilter' ).BClist()
        self.assertTrue( self.res == [['a','b','c'],['me','you','he','her','it']] )
        
    def testSub3(self):
        self.res = self.BC.BCsub( 'BCmapfilter', lambda i:i*2 ).BClist()
        self.assertTrue( self.res == [['aa','bb','cc'],['meme','youyou','hehe','herher','itit']] )
        
    def testSub4(self):
        """can be made in a recursive way"""
        self.BC = BroadCaster([ [['a'],['b']], [['c'],['d']] ])
        self.res = self.BC.BCsub('BCsub', 'BCmapfilter', lambda i:i*2 ).BClist()
        self.assertTrue( self.res == [ [['aa'],['bb']], [['cc'],['dd']] ] )
        
    def testSub5(self):
        self.res = self.BC.BCsub( '__getitem__',0 ).BClist()
        self.assertTrue( self.res == [['a','b','c'],['m','y','h','h','i']] )

        
objs = ( globals()[text] for text in dir())
tests = list({ test for test in objs if type(test)==type and issubclass(test,unittest.TestCase) })
suites = [ unittest.makeSuite(test) for test in tests ]
suite = unittest.TestSuite(suites)
runner = unittest.TextTestRunner()
res = runner.run(suite)
for f,e in set(res.failures) | set(res.errors):
    print f,'\n',e,'\n'



import doctest
def test_documentation(obj,verbose=False, globs = globals()):
    """test the docstring of an object, a function or a module"""
    test = doctest.DocTestFinder().find(obj, globs=globs)
    runner = doctest.DocTestRunner(verbose=verbose)
    results = {}
    name = ''
    def out(s):
        results[name].append(s)
    for t in test:
        name = t.name
        results[name]=[]
        runner.run(t,out=out)
    if not verbose:
        rimuovi = [ k for k,v in results.iteritems() if not len(v) ]
        for k in rimuovi:
            del results[k]
    if results:
        raise Error('the documentation is outdated')
test_documentation(BroadCaster) 
