//
// Copyright 2015 by xamoom GmbH <apps@xamoom.com>
//
// This file is part of some open source application.
//
// Some open source application is free software: you can redistribute
// it and/or modify it under the terms of the GNU General Public
// License as published by the Free Software Foundation, either
// version 2 of the License, or (at your option) any later version.
//
// Some open source application is distributed in the hope that it will
// be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
// of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with xamoom-ios-sdk. If not, see <http://www.gnu.org/licenses/>.
//


#import "XMMContent.h"

@implementation XMMContent

+(RKObjectMapping *)mapping {
  RKObjectMapping* mapping = [RKObjectMapping mappingForClass:[XMMContent class] ];
  [mapping addAttributeMappingsFromDictionary:@{@"description":@"descriptionOfContent",
                                                @"language":@"language",
                                                @"title":@"title",
                                                @"image_public_url":@"imagePublicUrl",
                                                @"content_id":@"contentId",
                                                }];
  return mapping;
}

-(NSArray *)sortedContentBlocks {
  NSSortDescriptor *descriptor = [NSSortDescriptor sortDescriptorWithKey:@"order" ascending:YES];
  NSArray *sorting = @[descriptor];
  
  return [self.contentBlocks sortedArrayUsingDescriptors:sorting];
}

@end
