function ueScrollAccordion(){
  
    var g_scrollAccordion, g_scrollAccordionItems; 
    var g_classConnected;
    var g_isInEditor;

    /*
    * clone sections and append to their parent slides
    */
    function findSections(g_scrollAccordionItem, sectionToClone){  
      
      //clone section - use detach method on front to make elementor widgets work
      var clonedSectionItem = sectionToClone.detach();
      
      //paste section
      var saItemContentWrapper = g_scrollAccordionItem.find(".ue_content_wrapper.ue_section_id");

      saItemContentWrapper.html(clonedSectionItem);
      
      //add connected class to scroll accordion child element
      var g_scrollAccordionSection = g_scrollAccordionItem.children();
      
      g_scrollAccordionSection.addClass(g_classConnected);
      
    }
    
    /*
    * show what sections are connected to scroll accordion in editor
    */
    function findSectionsInEditor(g_scrollAccordionItem){     
      
      //cloned section's id
      var g_scrollAccordionItemId = g_scrollAccordionItem.data("id");

      var scrollAccordionItemSource = g_scrollAccordionItem.data("source");

      var saItemContentWrapper = g_scrollAccordionItem.find(".ue_content_wrapper.ue_section_id");

      if(scrollAccordionItemSource !== "section_id")
      return(false);
      
      g_scrollAccordionItem.addClass('uc-item-message');

      //scroll accordion item message in editor
      var g_scrollAccordionItemHTML = "<div class='uc-message'>Section with id <b>'" + g_scrollAccordionItemId + "'</b> connected to scroll accordion</div>";
      
      //paste section
      saItemContentWrapper.html(g_scrollAccordionItemHTML);
      
    }
    
    /*
    * handle section find error 
    */
    function showHideErrors(g_scrollAccordionItem, scrollAccordionItemId, sectionToClone) {
      
      var showErrors = g_scrollAccordion.data("errors");
      var scrollAccordionItemSource = g_scrollAccordionItem.data("source");
      var saItemContentWrapper = g_scrollAccordionItem.find(".ue_content_wrapper.ue_section_id");
      
      if (!g_isInEditor) {
        if (showErrors === false) {
            return(false);
        }
      }
      
      if(scrollAccordionItemSource !== "section_id")
      return(false);

      //check if section with id from scroll accordion item exist
      if(sectionToClone.length > 0)
      return(false);
      
      //if section with id from scroll accordion item does not exist, then add error clas to scroll accordion item
      g_scrollAccordionItem.addClass('uc-item-error');
      
      //add error html element
      saItemContentWrapper.html("<div class='uc-section-error'><div class='uc-error'>Couldn't find a section with id: '" + scrollAccordionItemId + "'</div></div>");
      
    }
    
    /*
    * show | hide section in editor
    */ 
    function hideSectionInEditor(sectionToClone){
      
      if(g_isInEditor == false)
      return(false);
    
      //affect only section that are not in connected to scroll accordion
      if(sectionToClone.hasClass(g_classConnected) == true)
      return(false);
      
      var dataShowInEditor = g_scrollAccordion.data('show-section');
      
      if(dataShowInEditor == 'no')
      sectionToClone.css('display', '');
      
      if(dataShowInEditor == 'hide')
      sectionToClone.hide();     
    }
    
    /*
    * define item type "section" behaviour on live page
    */
    function handleItemTypeSection(){
      
      g_scrollAccordionItems.each(function(){
        
        var g_scrollAccordionItem = jQuery(this); 

        var scrollAccordionItemId = g_scrollAccordionItem.data("id");
        
        //find sections to clone on the page
        var sectionToClone = jQuery("#" + scrollAccordionItemId);
        
        //clone and paste section from elementor layout
        findSections(g_scrollAccordionItem, sectionToClone);  

        var scrollAccordionItemSource = g_scrollAccordionItem.data("source");
        if(scrollAccordionItemSource !== "section_id")
        return;
        
        //see if scroll accordion item id has its element on the page
        showHideErrors(g_scrollAccordionItem, scrollAccordionItemId, sectionToClone);
        
      }); 
      
    }
    
    
    /*
    * define item type "section" behaviour in editor
    */
    function handleItemTypeSectionInEditor(){
      
      g_scrollAccordionItems.each(function(){
        
        var g_scrollAccordionItem = jQuery(this); 

        var scrollAccordionItemId = g_scrollAccordionItem.data("id");
        
        //find sections to clone on the page
        var sectionToClone = jQuery("#" + scrollAccordionItemId);
        
        //tell to user which section is connected
        findSectionsInEditor(g_scrollAccordionItem);
        
        //see if scroll accordion item id has its element on the page
        showHideErrors(g_scrollAccordionItem, scrollAccordionItemId, sectionToClone);
        
        //show | hide sections if needed
        hideSectionInEditor(sectionToClone);
        
      }); 
      
    }
    
    
    /*
    * init scroll accordion
    */
    this.init = function(objScrollAccordion){
      
      //init globals
      g_scrollAccordion = jQuery(objScrollAccordion);
      g_scrollAccordionItems = g_scrollAccordion.find('.ue_scroll_accordion_item');
      
      g_classConnected = 'uc-connected';
      g_activeSliderClass = '.uc-active-item';
      
      g_isInEditor = g_scrollAccordion.data("editor");
      
      //do not run scroll accordion in editor
      if(g_isInEditor == "no")
      handleItemTypeSection();    
      
      //in editor run a different function that do not manipulate DOM
      if(g_isInEditor == "yes")
      handleItemTypeSectionInEditor();
    }
  }