package com.xamoom.android.mapping;

import com.xamoom.android.APICallback;

/**
 * Used for mapping contentByLocationIdentifier responses from the xamoom-cloud-api.
 * ContentByLocationIdentifier will have a systemName, a systemUrl, a systemId,
 * a hasContent, a hasSpot, a content and/or style and/or menu if you want.
 *
 * @author Raphael Seher
 *
 * @see Content
 * @see Style
 * @see Menu
 * @see com.xamoom.android.XamoomEndUserApi#getContentByLocationIdentifier(String, String, boolean, boolean, String, APICallback)
 */
public class ContentByLocationIdentifier {

    private String systemName;
    private String systemUrl;
    private String systemId;
    private boolean hasContent;
    private boolean hasSpot;
    private Content content;
    private Style style;
    private Menu menu;

    @Override
    public String toString () {
       return (String.format("systemName: %s, " +
               "\nsystemUrl: %s, " +
               "\nsystemId: %s, " +
               "\nhasContent: %s, " +
               "\nhasSpot: %s, " +
               "\ncontent: %s, " +
               "\nstyle: %s, " +
               "\nmenu: %s", systemName, systemUrl, systemId, hasContent, hasSpot, content, style, menu));
    }

    public String getSystemName() {
        return systemName;
    }

    public String getSystemUrl() {
        return systemUrl;
    }

    public String getSystemId() {
        return systemId;
    }

    public boolean isHasContent() {
        return hasContent;
    }

    public boolean isHasSpot() {
        return hasSpot;
    }

    public Content getContent() {
        return content;
    }

    public Style getStyle() {
        return style;
    }

    public Menu getMenu() {
        return menu;
    }
}
