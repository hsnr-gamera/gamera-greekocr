# -*- mode: python; indent-tabs-mode: nil; tab-width: 3 -*-
# vim: set tabstop=3 shiftwidth=3 expandtab:

# Copyright (C) 2010-2011 Christian Brandt
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from gamera.core import *    
from gamera.plugins.pagesegmentation import textline_reading_order
from gamera.toolkits.ocr.ocr_toolkit import *
from gamera.toolkits.ocr.classes import Textline,Page,ClassifyCCs
import gamera.kdtree as kdtree
import unicodedata
import sys

class SinglePage(Page):      
   def lines_to_chars(self):
      subccs = self.img.sub_cc_analysis(self.ccs_lines)
      
      for i,segment in enumerate(self.ccs_lines):
         self.textlines.append(SingleTextline(segment, subccs[1][i]))



class Character(object):
   def __init__(self, glyph):
      self.maincharacter = glyph
      self.unicodename = glyph.get_main_id()
      self.unicodename = self.unicodename.replace(".", " ").upper()
      #print self.unicodename
      #self.unicodename = 
      self.combinedwith = []
      #print self.maincharacter
      
   def addCombiningDiacritics(self, diacrit):
      self.combinedwith.append(diacrit)
      pass
   
   def toUnicodeString(self):
      try:
         str = ""
         mainids = self.maincharacter.get_main_id().split(".and.")
         for char in mainids:
            if char == "skip" or char == "unclassified":
               continue
            str = str + "%c" % return_char(char)
               
         #str = u"" + return_char(self.unicodename)
         for char in self.combinedwith:
            #char = char.get_main_id().replace(".", " ").upper()
            mainids = char.get_main_id().split(".and.")
            #print mainids
            for char in mainids:
               if char == "skip":
                  continue
               #print "added %s to output" % char
               str = str + "%c" % return_char(char)
      
         return unicodedata.normalize('NFD', str)
      except:
         #print self.unicodename
         return "E"
         
      
      
class SingleTextline(Textline):
   def sort_glyphs(self):
      self.glyphs.sort(key=lambda x: x.ul_x)
      
      #begin calculating threshold for word-spacing
      glyphs = []
      for g in self.glyphs:
         if self.is_combining_glyph(g):
            continue
         
         glyphs.append(g)
         
      spacelist = []
      total_space = 0
      for i in range(len(glyphs) - 1):
         spacelist.append(glyphs[i + 1].ul_x - glyphs[i].lr_x)
      if(len(spacelist) > 0):
         threshold = median(spacelist)
         threshold = threshold * 2.0
      else:
         threshold  = 0
      #end calculatin threshold for word-spacing
      
      self.words = chars_make_words(self.glyphs, threshold)



   def is_combining_glyph(self, glyph):
      ret =  glyph.get_main_id().find("combining") != -1
      return ret
   


   def to_string(self):
      k = 3
      max_k = 10
      output = ""
      for word in self.words:
         med_center = median([g.center.y for g in word])
         glyphs_combining = []
         characters = []
         nodes_normal = []
         skipids = ["manual.xi.upper", "manual.xi.lower", "manual.theta.outer", "_split.splitx", "skip"]
         for glyph in word:
            mainid = glyph.get_main_id()
            
            if skipids.count(mainid) > 0:
               continue
            elif mainid == "manual.xi.middle":
               glyph.classify_automatic("greek.capital.letter.xi")
            elif mainid == "manual.theta.inner":
               glyph.classify_automatic("greek.capital.letter.theta")
            elif mainid == "comma" or mainid == "combining.comma.above":
               #print "%s - center_y: %d - med_center: %d" % (mainid, glyph.center.y, med_center)
               if glyph.center.y > self.bbox.center.y:
                  glyph.classify_automatic("comma")
               else:
                  glyph.classify_automatic("combining.comma.above")
            
            elif mainid.find("manual") != -1 or mainid.find("split") != -1:
               continue
            
            if self.is_combining_glyph(glyph):
               glyphs_combining.append(glyph)
            else:
               c = Character(glyph)
               characters.append(c)
               #print c
               nodes_normal.append(kdtree.KdNode((glyph.center.x, glyph.center.y), c))
         
         if (nodes_normal == None or len(nodes_normal) == 0):
            continue
            
         tree = kdtree.KdTree(nodes_normal)
         
         for g in glyphs_combining:
            fast = True
            if fast:
               knn = tree.k_nearest_neighbors((g.center.x, g.center.y), k)
               knn[0].data.addCombiningDiacritics(g)
            else:
               found = False
               while (not found) and k < max_k:
                  knn = tree.k_nearest_neighbors((g.center.x, g.center.y), k)
                  
                  for nn in knn:
                     if (nn.data.maincharacter.get_main_id().split(".").count("greek") > 0) and not found:
                        nn.data.addCombiningDiacritics(g)
                        found = True
                        break
               
                  k = k + 2      
                  
               
         for c in characters:
            output = output + c.toUnicodeString()
            
         output = output + " "



      return output


