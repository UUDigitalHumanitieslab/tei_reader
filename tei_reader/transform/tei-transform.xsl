<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" indent="yes"/>
    <xsl:template match="/">
        <corpus>
            <xsl:for-each select="TEI">
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
    <xsl:template match="encodingDesc|fileDesc|profileDesc">
        <attributes key="{name(.)}">
            <xsl:for-each select="*[not(name()='classDecl')]">
                <attribute key="{name(.)}">
                    <xsl:apply-templates />
                </attribute>
            </xsl:for-each>
            <xsl:apply-templates select="classDecl" />
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
    <xsl:template match="addrLine|address|author|bibl|biblStruct|body|classCode|div|edition|extent|funder|head|imprint|item|keywords|list|monogr|p|principal|pubPlace|pubPlace|publisher|publisher|refState|respStmt|sponsor|text">
        <div tei-tag="{name(.)}">
            <xsl:call-template name="id" />
            <xsl:call-template name="attributes" />
            <xsl:apply-templates />
        </div>
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
    <xsl:template match="date|emph|hi|l|language|lg|name|q|resp|term|title">
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
</xsl:stylesheet>