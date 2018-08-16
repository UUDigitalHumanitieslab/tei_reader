<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" indent="yes"/>
    <xsl:template match="/">
        <corpus>
            <xsl:for-each select="TEI|TEI.2">
                <document>
                    <xsl:call-template name="id" />
                    <xsl:apply-templates select="teiHeader" />
                    <xsl:apply-templates select="div|text" />
                </document>
            </xsl:for-each>
        </corpus>
    </xsl:template>
    <xsl:template match="teiHeader">
        <xsl:apply-templates />
    </xsl:template>
    <xsl:template match="encodingDesc|fileDesc|sourceDesc|profileDesc">
        <attributes key="{name(.)}">
            <xsl:for-each select="*">
                <attribute key="{name(.)}">
                    <xsl:call-template name="attributes-from-elements" /> 
                </attribute>
            </xsl:for-each>
        </attributes>
    </xsl:template>
    <xsl:template match="revisionDesc">
        <attributes key="{name(.)}">
            <xsl:for-each select="change">
                <attribute>
                    <xsl:attribute name="key">change_<xsl:number /></xsl:attribute>
                    <attributes>
                        <xsl:call-template name="attributes-id" />
                        <xsl:call-template name="attributes-pairs" />
                    </attributes>
                    <xsl:apply-templates />
                </attribute>
            </xsl:for-each>
        </attributes>
    </xsl:template>
    <xsl:template match="figure">
        <div tei-tag="{name(.)}">
            <attributes>
                <xsl:for-each select="graphic/@*[not(name() = 'xml:id')]">
                    <attribute key="{name()}">
                        <xsl:value-of select="." />
                    </attribute>
                </xsl:for-each>
            </attributes>
            <xsl:call-template name="id" />
            <xsl:call-template name="attributes" />
            <xsl:apply-templates />
        </div>
    </xsl:template>
    <xsl:template match="addrLine|address|author|bibl|biblStruct|body|classCode|div|edition|extent|funder|head|imprint|item|keywords|list|listBibl|monogr|p|principal|pubPlace|pubPlace|publisher|publisher|refState|respStmt|sponsor|text">
        <div tei-tag="{name(.)}">
            <xsl:call-template name="id" />
            <xsl:call-template name="attributes" />
            <xsl:apply-templates />
        </div>
    </xsl:template>
    <!-- these page and line beginnings are processed by the reader -->
    <xsl:template match="lb|pb">
        <xsl:element name="{name(.)}">
            <xsl:attribute name="tei-tag">
                <xsl:value-of select="name(.)"/>
            </xsl:attribute>
            <xsl:call-template name="id" />
            <xsl:call-template name="attributes" />
        </xsl:element>
    </xsl:template>
    <!-- elements used in editorialDecl, refsDecl -->
    <xsl:template match="correction|hyphenation|interpretation|normalization|punctuation|quotation|segmentation|stdVals|cRefPattern|refState">
        <attributes key="{name(.)}">
            <xsl:call-template name="attributes-id" />
            <xsl:call-template name="attributes-pairs" />
            <xsl:if test="*">
                <attribute>
                    <xsl:apply-templates />
                </attribute>
            </xsl:if>
        </attributes>
    </xsl:template>
    <xsl:template match="classDecl|taxonomy">
        <attribute key="{name(.)}">
            <attributes>
                <xsl:for-each select="taxonomy">
                    <attribute>                    
                        <xsl:attribute name="key">
                            <xsl:value-of select="@xml:id"/>
                        </xsl:attribute>
                        <xsl:apply-templates />
                    </attribute>
                </xsl:for-each>
            </attributes>
        </attribute>
    </xsl:template>
    <xsl:template match="date|emph|hi|l|language|lg|name|q|resp|term|title|w">
        <part tei-tag="{name(.)}">
            <xsl:call-template name="id" />
            <xsl:call-template name="attributes" />
            <xsl:apply-templates />
        </part>
    </xsl:template>
    <xsl:template match="note">
        <attributes>
            <attribute key="note">
                <xsl:apply-templates />
            </attribute>
        </attributes>
    </xsl:template>
    <xsl:template name="id">
        <xsl:if test="@xml:id">
            <xsl:attribute name="id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
        </xsl:if>
    </xsl:template>
    <xsl:template name="attributes">
        <xsl:if test="@*[not(name() = 'xml:id')]">
            <attributes>
                <xsl:call-template name="attributes-pairs" />
            </attributes>
        </xsl:if>
        <xsl:if test="name(following-sibling::*[1])='note'">
            <xsl:apply-templates select="following-sibling::note" />
        </xsl:if>
    </xsl:template>
    <!-- <attribute> containing the xml:id -->
    <xsl:template name="attributes-id">
        <xsl:if test="@xml:id">
            <attribute key="id">
                <xsl:value-of select="@xml:id"/>
            </attribute>
        </xsl:if>
    </xsl:template>
    <!-- <attribute> for each attribute pair in the element -->
    <xsl:template name="attributes-pairs">
        <xsl:for-each select="@*[not(name() = 'xml:id')]">
            <attribute key="{name()}">
                <xsl:value-of select="." />
            </attribute>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="attributes-as-parts">
        <xsl:for-each select="@*[not(name() = 'xml:id')]">
            <part tei-tag="@{name()}">
                <xsl:value-of select="." />
            </part>
        </xsl:for-each>
    </xsl:template>
    <!-- <attribute> for each subelement -->
    <xsl:template name="attributes-from-elements">
        <!-- variables not supported, update it manually
             <xsl:variable name="textNodes" select="p|text|date"/> -->
        <xsl:call-template name="id" />
        <xsl:if test="*[not(self::p)][not(self::text)][not(self::date)] | @*[not(name() = 'xml:id')]">
            <attributes>
                <xsl:call-template name="attributes-pairs" />
                <xsl:for-each select="*[not(self::p)][not(self::text)][not(self::date)]">
                    <attribute key="{name()}">
                        <xsl:call-template name="attributes-from-elements" />
                    </attribute>
                </xsl:for-each>
            </attributes>
        </xsl:if>
        <xsl:value-of select="text()"/>
        <xsl:apply-templates select="p|text|date" />
    </xsl:template>
</xsl:stylesheet>
