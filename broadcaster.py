 
import itertools as it
import sys
import re

#aggiungere qualcosa per le regex?
# re.sub
# re.findall
# re.split

class BroadCaster(object):

    def __init__(self,iterable):
        """
        create the BroadCaster from an iterable upon which is going to broadcast some operation
        """
        self.iter = iter(iterable)
        
    def __iter__(self):
        """
        Return an iterable of itself. It allow the Broadcaster to be used on cycles.
        
        >>> for i in BroadCaster([1,2,3]): print i
        1
        2
        3
        """
        return self
        
    def next(self):
        """allow the iteration over itself"""
        return next(self.iter)
    
    def __getattr__(self,item):
        """implicit method to obtain an attribute, doesn't apply magic methods (but they can be called directly)"""
        return BroadCaster( i.__getattribute__(item) for i in self )
    
    def __call__(self,*args,**kwargs):
        """redirect the calling methods, needed to broadcast the calling of a method"""
        return BroadCaster( i(*args,**kwargs) for i in self )
    
    def __getitem__(self,indices):
        """get one or more secondary elements from the element in the sequence"""
        if hasattr(indices,'__iter__'):
            return BroadCaster( [ i[idx] for idx in indices ] for i in self )
        else:
            return BroadCaster( i[indices] for i in self )
    
    #def BCend(self):
    #    """burn the whole iterator"""
    #    for i in self:
    #        pass
    
    def BClist(self):
        """convert the inner iterable to a list"""
        return list(self)
    
    def BCset(self):
        """convert the inner iterable to a set"""
        return set(self)
    
    def BCmapfilter(self,map=None,filter=None):
        """implement a map and filter generator"""
        omap = map
        map = (lambda i:i) if (map is None) else map
        filter = (lambda i:True) if (filter is None) else filter
        return BroadCaster( map(i) for i in self if filter(i) )
    
    def BCpairwise(self, func, default=None, accumulate=False):
        """apply a function to the element of the iterator in a paiwise manner"""
        def accumulator():
            old = next(self) if default is None else default
            for new in self:
                val = func(old,new)
                yield val
                old = val if accumulate else new
        return BroadCaster(accumulator())
    
    def BCapply(self,function,*args,**kwargs):
        """apply a function to the whole iterator"""
        return BroadCaster(function(self,*args,**kwargs))
    
    def BCflatten(self):
        """return the flat version of self"""
        def flatter(elem):
            try:
                for i in elem:
                    yield i
            except TypeError:
                yield elem
        return BroadCaster( i for elem in self for i in flatter(elem) )
        
    def BCformat(self,format="{}",separator=" ",stdout=sys.stdout):
        """print over the given writable output the representation of the iterator"""
        def echo(idx,i):
            stdout.write((separator if idx else "")+format.format(i))
            return i
        return BroadCaster( echo(idx,i) for idx,i in enumerate(self))
    
    def BCtranspose(self,**kwargs):
        """transpose the Broadcaster"""
        try:
            fillvalue = kwargs['fillvalue']
            return BroadCaster( list(i) for i in it.izip_longest(*(self.BClist()),fillvalue=fillvalue))
        except KeyError:
            return BroadCaster( list(i) for i in it.izip(*(self.BClist())))
        
    def BCsplit(self,pieces=0,**kwargs):
        """split self into chunks of the given length. If 0 it return the flat version."""
        flat = self.BCflatten()
        if pieces==0: return flat
        try:
            fillvalue = kwargs['fillvalue']
            return BroadCaster( list(i) for i in it.izip_longest(*([flat] * pieces),fillvalue=fillvalue) )
        except KeyError:
            return BroadCaster( list(i) for i in zip(*([flat] * pieces)) )
    
    def BCsub(self,func_name,*args,**kwargs):
        """apply the given function to the sublist, after converting it to a BroadCaster and back
        can be recursive!!"""
        if func_name in BroadCaster.__dict__:
            return BroadCaster( BroadCaster(i).__getattribute__(func_name)(*args,**kwargs).BClist() for i in self )
        return BroadCaster( BroadCaster(i).__getattr__(func_name)(*args,**kwargs).BClist() for i in self )